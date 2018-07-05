import datetime
import json
import logging

from flask import request
from flask_restplus import Resource
from api.serializers import movie, page_of_movies
from api.parsers import pagination_arguments
from api.api import api

from services.producer_handler import AMovieRPC

logger = logging.getLogger(__name__)

amovies_namespace = api.namespace('amovies', description='Movies can be served here')

amovie_rpc = AMovieRPC()


@amovies_namespace.route('/')
@api.response(404, 'Movies not found.')
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
                filter_by_year = datetime.datetime.strftime(args.get('year'), "%Y")
                data.update({'filters': {'year': filter_by_year, }})
            movies_query = amovie_rpc.call(http_method='GET', data=data)
            correlation_id = json.loads(movies_query.decode('utf8'))
            if 'exception' in correlation_id:
                logger.warning(correlation_id['exception'])
                return {'exception': correlation_id['exception']}, correlation_id['code']
            elif 'correlation_id' in correlation_id:
                return correlation_id, 200
            else:
                return {'response': 'Empty response'}, 404
        except Exception as exc:
            logger.warning(exc)
            return None, 404

    @api.response(204, 'Movie successfully created.')
    @api.expect(movie)
    def post(self):
        """
        Make POST request to create new movie object.
        """
        try:
            response = amovie_rpc.call(data=request.json, http_method='POST').decode('utf8')
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return None, 204
        except Exception as exc:
            logger.warning(exc)
            return None, 404


@amovies_namespace.route('/<int:id>')
@api.response(404, 'Movie can not be found.')
class MovieItem(Resource):
    # @api.marshal_with(movie)
    def get(self, id):
        """
        Make specified GET request using ID to obtain particular movie item.
        """
        try:
            response = json.loads(amovie_rpc.call(id=id, http_method='GET').decode('utf8'))
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return response, 200
        except Exception as exc:
            logger.warning(exc)
            return None, 404

    @api.expect(movie)
    @api.response(204, 'Movie successfully updated.')
    def put(self, id):
        """
        Make PUT request to update particular movie item.
        """
        try:
            data = request.json
            response = amovie_rpc.call(id=id, data=data, http_method='PATCH').decode('utf8')
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return None, 204
        except Exception as exc:
            logger.warning(exc)
            return None, 404

    @api.response(200, 'Movie successfully deleted.')
    def delete(self, id):
        """
        Make DELETE request to remove movie item from movies database.
        """
        try:
            response = amovie_rpc.call(id=id, http_method='DELETE').decode('utf8')
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return None, 200
        except Exception as exc:
            logger.warning(exc)
            return None, 404
