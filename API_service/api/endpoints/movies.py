import json
import logging

from flask import request
from flask_restplus import Resource
from api.serializers import movie, page_of_movies
from api.parsers import pagination_arguments
from api.api import api

from services.producer_handler import MovieRPC

logger = logging.getLogger(__name__)

namespace = api.namespace('movies', description='Movies can be served here')

movie_rpc = MovieRPC()


@namespace.route('/')
@api.response(404, 'Movies not found.')
class MovieResource(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_movies)
    def get(self):
        """
        Make GET request to obtain a list of available movies.
        """
        try:
            args = pagination_arguments.parse_args(request)
            page = args.get('page', 1)
            per_page = args.get('per_page', 10)
            data = {'page': page, 'per_page': per_page}
            movies_query = movie_rpc.call(http_method='GET', data=data)
            movies_page = json.loads(movies_query.decode('utf8'))
            if 'exception' in movies_page:
                logger.warning(movies_page['exception'])
                return {'error': movies_page['exception']}, movies_page['code']
            else:
                return movies_page
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
            response = movie_rpc.call(data=request.json, http_method='POST').decode('utf8')
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'error': response['exception']}, response['code']
            else:
                return None, 204
        except Exception as exc:
            logger.warning(exc)
            return None, 404


@namespace.route('/<int:id>')
@api.response(404, 'Movie can not be found.')
class MovieItem(Resource):
    @api.marshal_with(movie)
    def get(self, id):
        """
        Make specified GET request using ID to obtain particular movie item.
        """
        try:
            response = json.loads(movie_rpc.call(id=id, http_method='GET').decode('utf8'))
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'error': response['exception']}, response['code']
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
            response = movie_rpc.call(id=id, data=data, http_method='PATCH').decode('utf8')
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'error': response['exception']}, response['code']
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
            response = movie_rpc.call(id=id, http_method='DELETE').decode('utf8')
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'error': response['exception']}, response['code']
            else:
                return None, 200
        except Exception as exc:
            logger.warning(exc)
            return None, 404
