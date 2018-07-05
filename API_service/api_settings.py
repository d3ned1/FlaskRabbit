import logging
import os

logging_format = ' %(asctime)s | %(levelname)s | %(name)s | %(lineno)d | %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)

basedir = os.path.abspath(os.path.dirname(__file__))

FLASK_SERVER_NAME = 'localhost:8001'
FLASK_DEBUG = False  # Do not use debug mode in production

RABBIT_HOST = 'localhost'
RABBIT_PORT = 5672

RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

REDIS_HOST = 'localhost'
REDIS_DB = 15
REDIS_PORT = 6379
