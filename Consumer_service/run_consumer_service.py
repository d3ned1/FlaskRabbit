import logging
from flask import Flask
from Consumer_service import settings
from Consumer_service.models.movie import db
from Consumer_service.services.receive import ConsumerRPC

app = Flask(__name__)

logger = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app, migrate=False):
    configure_app(flask_app)
    db.init_app(flask_app)
    flask_app.app_context().push()
    start_consumer = ConsumerRPC()
    start_consumer.call()

    if migrate:
        return app


def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
