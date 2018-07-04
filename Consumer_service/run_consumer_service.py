import logging
from threading import Thread

from flask import Flask

import consumer_settings
from models.movie import db
from services.cache_handler import RedisConsumerRPC
from services.consumer_handler import ConsumerRPC

app = Flask(__name__)

logger = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = consumer_settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = consumer_settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = consumer_settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = consumer_settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = consumer_settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = consumer_settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = consumer_settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app, migrate=False):
    configure_app(flask_app)
    db.init_app(flask_app)
    if not migrate:
        # start_consumer_1 = ConsumerRPC()
        # thread = Thread(target=start_consumer_1.call, args=(flask_app, ), daemon=True)
        # thread.start()
        # start_consumer_1.call(app)

        start_consumer_2 = RedisConsumerRPC()
        # thread2 = Thread(target=start_consumer_2.call, args=(flask_app, ), daemon=True)
        # thread2.start()
        start_consumer_2.call(app)

    if migrate:
        return app


def main():
    initialize_app(app)
    app.run(debug=consumer_settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
