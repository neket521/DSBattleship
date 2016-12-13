import uuid
import pika
from common import REQ_CONNECT, REQ_EXIT

class Client:

    ___NAME = 'Battleship Game'
    ___VER = '0.1'
    ___BUILT = '2016-12-13'
    ___VENDOR = 'Copyright (c) Anton Prokopov, Nikita Kirienko'
    ___EXIT_COMMAND = 'Type \'exit\' to leave the game'

    def info(self):
        return '%s version %s (%s) %s\n%s' % (Client.___NAME, Client.___VER, Client.___BUILT, Client.___VENDOR, Client.___EXIT_COMMAND)

    def __init__(self, server):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, reqCode):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue_durable',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(reqCode) + ':' + 'empty_body')
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def connect(self):
        connect_request = REQ_CONNECT
        return self.call(connect_request)

    def exit_game(self):
        exit_request = REQ_EXIT
        return self.call(exit_request)

client = Client("127.0.0.1")
print client.info()
print client.connect()
try:
    print 'Falling to loop...'
    while 1:
        if raw_input() == 'exit':
            print client.exit_game()
            break
except KeyboardInterrupt:
    print client.exit_game()