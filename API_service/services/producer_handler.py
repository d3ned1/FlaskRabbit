import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
exchange_name = 'exchange.name'
routing_key = 'exchange.name'

channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)


def emit_data_get(id):
    method = 'GET'
    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=json.dumps([id, method]),
                          properties=pika.BasicProperties(delivery_mode=2))

    print("%r sent to exchange %r with data %s using method %s" % (routing_key, exchange_name, data, method))


def emit_data_update(id, data):
    method = 'PATCH'
    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=json.dumps([id, data, method]),
                          properties=pika.BasicProperties(delivery_mode=2))

    print("%r sent to exchange %r with data %s using method %s" % (routing_key, exchange_name, data, method))
    connection.close()


def emit_data_delete(data):
    method = 'DELETE'
    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=json.dumps([data, method]),
                          properties=pika.BasicProperties(delivery_mode=2))

    print("%r sent to exchange %r with data %s using method %s" % (routing_key, exchange_name, data, method))
    connection.close()


def emit_data_create(data):
    method = 'POST'
    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=json.dumps([data, method]),
                          properties=pika.BasicProperties(delivery_mode=2))

    print("%r sent to exchange %r with data %s using method %s" % (routing_key, exchange_name, data, method))
    connection.close()
