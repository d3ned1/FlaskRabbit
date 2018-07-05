import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

logging_format = ' %(asctime)s | %(levelname)s | %(name)s | %(lineno)d | %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)


SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'mydb'
USER = 'postgres'
PASSWORD = ''

SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(USER,
                                                                    PASSWORD,
                                                                    DB_HOST,
                                                                    DB_PORT,
                                                                    DB_NAME)

FLASK_SERVER_NAME = 'localhost:8000'
FLASK_DEBUG = False  # Do not use debug mode in production

RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

REDIS_HOST = 'localhost'
REDIS_DB = 15
REDIS_PORT = 6379
