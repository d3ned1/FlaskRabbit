import logging

from flask import request
from flask_restplus import Resource
from API_service.api.serializers import movie, page_of_movies
from API_service.api.parsers import pagination_arguments
from API_service.api.api import api
from API_service.models.movie import Movie

from API_service.services.producer_handler import emit_data_update, emit_data_create, emit_data_delete, emit_data_get

log = logging.getLogger(__name__)

namespace = api.namespace('movies', description='Movies can be served here')


@namespace.route('/')
class MovieResource(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_movies)
    def get(self):
        """
        Returns list of movies.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        emit_data_get(id=None)
        movies_query = Movie.query
        movies_page = movies_query.paginate(page, per_page, error_out=False)

        return movies_page

    @api.expect(movie)
    def post(self):
        """
        Create new movie.
        """
        emit_data_create(request.json)
        return None, 201


@namespace.route('/<int:id>')
@api.response(404, 'Movie can not be found.')
class MovieItem(Resource):

    @api.marshal_with(movie)
    def get(self, id):
        """
        Return movie item.
        """
        emit_data_get(id)

    @api.expect(movie)
    @api.response(204, 'Movie successfully updated.')
    def put(self, id):
        """
        Update movie item.
        """
        data = request.json
        emit_data_update(id, data)
        return None, 204

    @api.response(204, 'Movie successfully deleted.')
    def delete(self, id):
        """
        Deletes movie item.
        """
        emit_data_delete(id)
        return None, 204