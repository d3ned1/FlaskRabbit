import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

logging_format = ' %(asctime)s | %(levelname)s | %(name)s | %(lineno)d | %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)


SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:d3ned1xxx@localhost:5432/mydb"

FLASK_SERVER_NAME = 'localhost:8000'
FLASK_DEBUG = True  # Do not use debug mode in production

RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
