import uuid
import pika
from common import STATUS_CONNECTED, STATUS_EXIT, STATUS_LOGIN_FAIL, STATUS_CHOOSE_GAME, STATUS_GAME_SELECTED

class Client:

    ___NAME = 'Battleship Game'
    ___VER = '0.1'
    ___BUILT = '2016-12-13'
    ___VENDOR = 'Copyright (c) Anton Prokopov, Nikita Kirienko'
    ___EXIT_COMMAND = 'Type \'exit\' to leave the game'

    login = None
    status = -1

    def info(self):
        return '%s version %s (%s) %s\n%s' % (Client.___NAME, Client.___VER, Client.___BUILT, Client.___VENDOR, Client.___EXIT_COMMAND)

    def __init__(self, server):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def start_game(self):
        login = raw_input('Enter user login and press Enter:\n')
        print self.connect(login)
        if Client.status != STATUS_LOGIN_FAIL:
            # remember login to use it, when disconnecting
            Client.login = login

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            Client.status = int(body.split(':')[0])
            self.response = body.split(':')[1]

    def call(self, reqCode, body='empty_body'):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(reqCode) + ':' + body)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def connect(self, login):
        request_code = STATUS_CONNECTED
        return self.call(request_code, login)

    def exit_game(self, login):
        request_code = STATUS_EXIT
        if login != None:
            return self.call(request_code, login)
        else:
            return None

    def get_list_of_active_games(self):
        request_code = STATUS_CHOOSE_GAME
        return self.call(request_code)

    def select_game(self, n):
        request_code = STATUS_GAME_SELECTED
        return self.call(request_code, n)

    def loop(self):
        try:
            print 'Falling to loop...'
            while 1:
                if Client.status == STATUS_LOGIN_FAIL:
                    self.start_game()
                    continue
                if Client.status == STATUS_CONNECTED:
                    print 'Choose a game to join from the list below:'
                    print client.get_list_of_active_games()
                    selected_game = raw_input('Type the number and press Enter:\n')
                    print self.select_game(selected_game)
                    continue
                if Client.status == STATUS_EXIT:
                    print 'You have been kicked'
                    break
                if raw_input() == 'exit':
                    print self.exit_game(Client.login)
                    break
        except KeyboardInterrupt:
            print self.exit_game(Client.login)

client = Client("127.0.0.1")
print client.info()
client.start_game()
client.loop()