from flask import Flask, Blueprint
import api_settings
from api.endpoints.movies import namespace
from api.api import api
import logging

app = Flask(__name__)

logger = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = api_settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = api_settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = api_settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = api_settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = api_settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(namespace)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    app.run(debug=api_settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
