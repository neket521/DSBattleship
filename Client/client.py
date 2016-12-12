import uuid
import pika

class Client:
    def __init__(self, server):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=server))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()

        return self.response

    def is_connected(self):
        connect_request = "connect"
        connect_responce = self.call(connect_request)
        return connect_responce

client = Client("127.0.0.1")
print client.is_connected()
