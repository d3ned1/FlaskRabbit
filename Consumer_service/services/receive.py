import json
import pika

from Consumer_service.models.movie import Movie
from Consumer_service.resources.movieResource import create_movie, delete_movie, update_movie
from Consumer_service.run_consumer_service import initialize_app, app

app = initialize_app(app, migrate=True)
app.app_context().push()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
exchange_name = 'exchange.name'
routing_key = 'exchange.name'

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic', durable=True)

result = channel.queue_declare(queue=routing_key, exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=exchange_name,
                   queue=queue_name)




def callback(ch, method, properties, body):
    try:
        body = json.loads(body.decode('utf8'))
        if hasattr(body, 'method'):
            method = body['method']
        if hasattr(body, 'data'):
            data = body['data']
        if hasattr(body, 'id'):
            id = body['id']
    except Exception as exc:
        pass  # TODO
    if body and method:
        if method == 'GET' and id:
            if id is not None:
                pass
            elif id is None:
                movies_query = Movie.query
        if method == 'POST' and data:
            create_movie(body['data'])
        if body['method'] == 'PATCH':
            update_movie(body['id'], )
        if body['method'] == 'DELETE':
            pass
        print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue=routing_key,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
