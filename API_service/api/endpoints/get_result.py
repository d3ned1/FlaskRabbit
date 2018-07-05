import json
import logging
import redis
from API_service import api_settings

from flask_restplus import Resource
from api.api import api

from services.producer_handler import AMovieRPC

logger = logging.getLogger(__name__)

get_result_movies_namespace = api.namespace('get_result', description='Movies can be served here')

movie_rpc = AMovieRPC()
redis_client = redis.Redis(host=api_settings.REDIS_HOST, port=api_settings.REDIS_PORT,
                                db=api_settings.REDIS_DB)


@get_result_movies_namespace.route('/<string:uuid>')
@api.response(404, 'Rusult can not be found.')
class MovieItem(Resource):

    def get(self, uuid):
        """
        Make specified GET request using ID to obtain particular movie item.
        """
        try:
            response = json.loads(redis_client.get(uuid))
            if 'exception' in response:
                logger.warning(response['exception'])
                return {'exception': response['exception']}, response['code']
            else:
                return response, 200
        except Exception as exc:
            logger.warning(exc)
            return None, 404
