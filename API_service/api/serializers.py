from flask_restplus import fields
from API_service.api.api import api

movie = api.model('Movie', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a certain movie'),
    'title': fields.String(required=True, description='Movie title'),
    'year': fields.Date(required=True, description='Production year'),
    'length': fields.Integer(required=True, description='Picture length (min)'),
    'rate': fields.Float(required=True, description='Movie IMDB rate'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_movies = api.inherit('Page of movies', pagination, {
    'items': fields.List(fields.Nested(movie))
})
