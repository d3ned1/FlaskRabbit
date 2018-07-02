import json
import pika

from Consumer_service.models.movie import Movie
from Consumer_service.resources.movieResource import create_movie, delete_movie, update_movie
from Consumer_service.run_consumer_service import initialize_app, app

app = initialize_app(app, migrate=True)
app.app_context().push()

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def process_body(id, data, http_method, ):
    response = 'Empty response'
    if http_method == 'GET':
        if id is not None:
            try:
                response = Movie.query.filter(Movie.id == id).one().serialize
            except Exception as exc:
                response = {'exception': str(exc)}
        elif id is None:
            try:
                movie_query = Movie.query.order_by('id').paginate(page=data['page'], per_page=data['per_page'])
                response = {
                "items": [i.serialize for i in movie_query.items],
                "page": movie_query.page,
                "pages": movie_query.pages,
                "per_page": movie_query.per_page,
                "total": movie_query.total
                }
            except Exception as exc:
                response = {'exception': str(exc)}
    if http_method == 'POST' and data:
        try:
            response = create_movie(data)
        except Exception as exc:
            response = {'exception': str(exc)}
    if http_method == 'PATCH' and id:
        try:
            response = update_movie(id, data)
        except Exception as exc:
            response = {'exception': str(exc)}
    if http_method == 'DELETE' and id:
        try:
            response = delete_movie(id)
        except Exception as exc:
            response = {'exception': str(exc)}
    return response


def on_request(ch, method, props, body):
    try:
        body = json.loads(body.decode('utf8'))
        print(" [ OK ] Received body %s  OK ]" % body)
    except Exception as exc:
        print(" [ ! ] Problem due to receiving: %exc [ ! ]" % exc)
    if body:
        http_method = body['method']
        data = body['data']
        id = body['id']
        response = process_body(id, data, http_method)
    else:
        response = {'error': 'Empty body received'}

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [ ? ] Waiting for requests [ ? ]")
channel.start_consuming()

# exchange_name = 'exchange.name'
# routing_key = 'exchange.name'
#
# channel.exchange_declare(exchange=exchange_name,
#                          exchange_type='topic', durable=True)
#
# result = channel.queue_declare(queue=routing_key, exclusive=True)
# queue_name = result.method.queue
#
# channel.queue_bind(exchange=exchange_name,
#                    queue=queue_name)
#
#
#
#

#
#
# channel.basic_consume(callback,
#                       queue=routing_key,
#                       no_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
