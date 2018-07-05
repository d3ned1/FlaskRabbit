import json
import logging
import threading
import time

import pika
import redis

from sqlalchemy import extract

import consumer_settings
from models.movie import Movie
from resources.movieResource import create_movie, delete_movie, update_movie

logger = logging.getLogger(__name__)


class ConsumerRPC(object):
    def __init__(self):
        self.response = {}
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=consumer_settings.RABBIT_HOST,
                                                                            port=consumer_settings.RABBIT_PORT))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='a_rpc_queue')
        self.redis_client = redis.Redis(host=consumer_settings.REDIS_HOST, port=consumer_settings.REDIS_PORT,
                                        db=consumer_settings.REDIS_DB)
        self.channel.basic_qos(prefetch_count=1)

    def call(self, flask_app):
        flask_app.app_context().push()
        self.channel.basic_consume(self.on_request, queue='a_rpc_queue')
        logger.info(" [ ... ] {} - Waiting for incoming data [ ... ]".format(threading.current_thread()))
        self.channel.start_consuming()

    def on_request(self, chan, method, props, body):
        chan.basic_publish(exchange='',
                           routing_key=props.reply_to,
                           properties=pika.BasicProperties(correlation_id=props.correlation_id,
                                                           content_type='application/json'
                                                           ),
                           body=json.dumps({'uuid': props.correlation_id}))
        chan.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(" [ <-- ] {} - Returned UUID {} [ OK ]".format(threading.current_thread(), props.correlation_id))

        try:
            body = json.loads(body.decode('utf8'))
            logger.info(" [ --> ] {} - Received body {} [ OK ]".format(threading.current_thread(), body))
        except Exception as exc:
            self.response = {'exception': 'Problem due to receiving: {}'.format(exc), 'code': 500}
            logger.warning(" [  !  ] {} - Problem due to receiving: {} [  !  ]".format(threading.current_thread(), exc))
        if body:
            http_method = body['method']
            data = body['data']
            item_id = body['item_id']
            try:
                self.response = self.prepare_body_for_redis(item_id, data, http_method, props)
            except Exception as exc:
                logger.warning(exc)
                self.response = {'exception': str(exc), 'code': 500}
        else:
            self.response = {'exception': 'Empty body received', 'code': 500}

    def prepare_body_for_redis(self, item_id, data, http_method, props):
        self.redis_client.set(props.correlation_id, json.dumps({'message': 'Please wait, task in progress ...'}))
        response = {'message': 'Please wait, task in progress ...'}
        time.sleep(5)
        if http_method == 'GET':
            if item_id is not None:
                try:
                    response = Movie.query.filter(Movie.id == item_id).one().serialize
                except Exception as exc:
                    logger.warning(exc)
                    response = {'exception': str(exc), 'code': 404}
            elif item_id is None:
                try:
                    if 'filters' in data:
                        filters = data['filters']
                        movie_query = Movie.query.filter(Movie.year == filters['year']) \
                            .order_by('year').paginate(
                            page=data['page'],
                            per_page=data['per_page'])
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
                response = {'id': create_movie(data)}
            except Exception as exc:
                response = {'exception': str(exc), 'code': 404}
                logger.warning(exc)
        if http_method == 'PATCH' and item_id:
            try:
                update_movie(item_id, data)
                response = {'message': 'successfully updated', 'data': data, 'code': 202}
            except Exception as exc:
                response = {'exception': str(exc), 'code': 404}
                logger.warning(exc)
        if http_method == 'DELETE' and item_id:
            try:
                delete_movie(item_id)
                response = {'message': 'successfully deleted', 'data': {'id': item_id}, 'code': 202}
            except Exception as exc:
                response = {'exception': str(exc), 'code': 404}
                logger.warning(exc)
        if 'exception' in response:
            self.redis_client.set(props.correlation_id, json.dumps(response))
        else:
            self.redis_client.set(props.correlation_id, json.dumps(response), 60)
        return response
