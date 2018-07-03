import logging
import traceback

from flask_restplus import Api
import api_settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version='0.1', title='Movie Service API',
          description='Flask RestPlus powered API')


@api.errorhandler
def default_error_handler(exception):
    message = 'Exception occurred.'
    log.exception(message)

    if not api_settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(exception):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404