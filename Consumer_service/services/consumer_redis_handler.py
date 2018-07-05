import json
import logging
import time

import pika
import redis

from sqlalchemy import extract

import consumer_settings
from models.movie import Movie
from resources.movieResource import create_movie, delete_movie, update_movie

logger = logging.getLogger(__name__)


def process_body_to_redis(id, data, http_method, ):
    time.sleep(10)
    response = 'Empty response'
    if http_method == 'GET':
        if id is not None:
            try:
                response = Movie.query.filter(Movie.id == id).one().serialize
            except Exception as exc:
                logger.warning(exc)
                response = {'exception': str(exc), 'code': 404}
        elif id is None:
            try:
                if 'filters' in data:
                    filters = data['filters']
                    movie_query = Movie.query.filter(extract('year', Movie.year) == filters['year'])\
                        .order_by('year').paginate(
                        page=data['page'],
                        per_page=data['per_page'])
                    response = {
                        "items": [i.serialize for i in movie_query.items],
                        "page": movie_query.page,
                        "pages": movie_query.pages,
                        "per_page": movie_query.per_page,
                        "total": movie_query.total
                    }
                else:
                    movie_query = Movie.query.order_by('id').paginate(page=data['page'], per_page=data['per_page'])
                    response = {
                        "items": [i.serialize for i in movie_query.items],
                        "page": movie_query.page,
                        "pages": movie_query.pages,
                        "per_page": movie_query.per_page,
                        "total": movie_query.total
                    }
            except Exception as exc:
                logger.warning(exc)
                response = {'exception': str(exc), 'code': 404}
    if http_method == 'POST' and data:
        try:
            response = create_movie(data)
        except Exception as exc:
            response = {'exception': str(exc), 'code': 404}
            logger.warning(exc)
    if http_method == 'PATCH' and id:
        try:
            response = update_movie(id, data)
        except Exception as exc:
            response = {'exception': str(exc), 'code': 404}
            logger.warning(exc)
    if http_method == 'DELETE' and id:
        try:
            response = delete_movie(id)
        except Exception as exc:
            response = {'exception': str(exc), 'code': 404}
            logger.warning(exc)
    return response


class RedisConsumerRPC(object):
    def __init__(self):
        self.response = {}
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='a_rpc_queue')
        self.redis_client = redis.Redis(host=consumer_settings.REDIS_HOST, port=consumer_settings.REDIS_PORT, db=consumer_settings.REDIS_DB)
        self.channel.basic_qos(prefetch_count=1)

    def call(self, flask_app):
        flask_app.app_context().push()
        self.channel.basic_consume(self.on_request, queue='a_rpc_queue')
        logger.info(" [ ... ] Waiting for incoming data [ ... ]")
        self.channel.start_consuming()

    def on_request(self, chan, method, props, body):
        chan.basic_publish(exchange='',
                           routing_key=props.reply_to,
                           properties=pika.BasicProperties(correlation_id=props.correlation_id,
                                                           content_type='application/json'
                                                           ),
                           body=json.dumps({'correlation_id': props.correlation_id}))
        chan.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(" [ <-- ]  Returned correlation id {} [ OK ]".format(props.correlation_id))

        try:
            body = json.loads(body.decode('utf8'))
            logger.info(" [ --> ] Received body {} [ OK ]".format(body))
        except Exception as exc:
            self.response = {'exception': 'Problem due to receiving: {}'.format(exc), 'code': 500}
            logger.warning(" [ ! ] Problem due to receiving: {} [ ! ]".format(exc))
        if body:
            http_method = body['method']
            data = body['data']
            id = body['id']
            try:
                self.redis_client.set(props.correlation_id, json.dumps({'message': 'Please wait, task in progress'}))
                self.response = process_body_to_redis(id, data, http_method)
                self.redis_client.set(props.correlation_id, json.dumps(self.response), 60)
            except Exception as exc:
                logger.warning(exc)
                self.response = {'exception': str(exc), 'code': 500}
        else:
            self.response = {'exception': 'Empty body received', 'code': 500}
