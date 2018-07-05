import json
import logging

from flask import request
from flask_restplus import Resource
from api.serializers import movie, page_of_movies
from api.parsers import pagination_arguments
from api.api import api
from services.producer_handler import MovieRPC

logger = logging.getLogger(__name__)

movies_namespace = api.namespace('movies', description='Movies queries can be served here. '
                                                       'Corresponded UUID will be returned.')
movie_rpc = MovieRPC()


@movies_namespace.route('/')
@api.response(404, 'Can not be found.')
class MovieResource(Resource):
    @api.response(200, 'Success.')
    @api.expect(pagination_arguments)
    def get(self):
        """
        Make GET request to obtain a list of available movies.
        """
        try:
            args = pagination_arguments.parse_args(request)
            page = args.get('page', 1)
            per_page = args.get('per_page', 10)
            data = {'page': page, 'per_page': per_page, }
            if args.get('year') and args.get('year') is not None:
                filter_by_year = args.get('year')
                data.update({'filters': {'year': filter_by_year, }})
            movies_query = movie_rpc.call(http_method='GET', data=data)
            uuid = json.loads(movies_query.decode('utf8'))
            if 'exception' in uuid:
                logger.warning(uuid['exception'])
                return {'exception': uuid['exception']}, uuid['code']
            elif 'uuid' in uuid:
                return uuid, 200
            else:
                return {'response': 'Empty response'}, 404
        except Exception as exc:
            logger.warning(exc)
            return None, 404

    @api.response(201, 'Token on item create successfully received.')
    @api.expect(movie)
    def post(self):
        """
        Make POST request to create new movie object.
        """
        try:
            response = movie_rpc.call(data=request.json, http_method='POST').decode('utf8')
            response = json.loads(response)
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return response, 201
        except Exception as exc:
            logger.warning(exc)
            return None, 404


@movies_namespace.route('/<int:item_id>')
@api.response(404, 'Can not be found.')
class MovieItem(Resource):
    @api.response(200, 'Token on item query successfully received.')
    def get(self, item_id):
        """
        Make specified GET request using ID to obtain particular movie item.
        """
        try:
            response = json.loads(movie_rpc.call(item_id=item_id, http_method='GET').decode('utf8'))
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return response, 200
        except Exception as exc:
            logger.warning(exc)
            return None, 404

    @api.expect(movie)
    @api.response(202, 'Token on item update successfully received.')
    def put(self, item_id):
        """
        Make PUT request to update particular movie item.
        """
        try:
            data = request.json
            response = json.loads(movie_rpc.call(item_id=item_id, data=data, http_method='PATCH'))
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return response, 202
        except Exception as exc:
            logger.warning(exc)
            return None, 404

    @api.response(202, 'Token on item remove successfully received.')
    def delete(self, item_id):
        """
        Make DELETE request to remove movie item from movies database.
        """
        try:
            response = json.loads(movie_rpc.call(item_id=item_id, http_method='DELETE'))
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return response, 202
        except Exception as exc:
            logger.warning(exc)
            return None, 404
