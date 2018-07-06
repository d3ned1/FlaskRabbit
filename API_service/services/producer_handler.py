import pika
import json
import uuid
import api_settings


class MovieRPC(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=api_settings.RABBIT_HOST,
                                                                            port=api_settings.RABBIT_PORT))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, channel, method, props, body):
        if self.correllation_id == props.correlation_id:
            self.response = body

    def call(self, item_id=None, http_method=None, data=None):
        self.correllation_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='a_rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.correllation_id,
                                       content_type='application/json'
                                       ),
                                   body=json.dumps({'item_id': item_id, 'method': http_method, 'data': data}))
        return json.dumps({'uuid': self.correllation_id})
