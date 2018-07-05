import json
import logging
import redis
from API_service import api_settings

from flask_restplus import Resource
from api.api import api

from services.producer_handler import MovieRPC

logger = logging.getLogger(__name__)

get_result_movies_namespace = api.namespace('get_result', description='One can obtain result using query UUID.')

movie_rpc = MovieRPC()
redis_client = redis.Redis(host=api_settings.REDIS_HOST, port=api_settings.REDIS_PORT,
                           db=api_settings.REDIS_DB)


@get_result_movies_namespace.route('/')
class Empty(Resource):
    def get(self):
        return {'message': 'Token must be provided /api/get_result/<uuid>'}, 404


@get_result_movies_namespace.route('/<string:uuid>')
@api.response(404, 'Result can not be found.')
class MovieItem(Resource):
    @api.response(200, 'Success.')
    def get(self, uuid):
        """
        Make specified GET request using ID to obtain particular movie item.
        """
        try:
            if redis_client.get(uuid) is not None:
                response = json.loads(redis_client.get(uuid))
                if 'exception' in response:
                    logger.warning(response['exception'])
                    return {'exception': response['exception']}, response['code']
                else:
                    return response, 200
            else:
                return {'message': 'Empty response. No data for given token'}, 404
        except Exception as exc:
            logger.warning(exc)
            return None, 404
