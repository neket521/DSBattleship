import pika
import sys
import time
import threading
from common import STATUS_CONNECTED, STATUS_EXIT, STATUS_LOGIN_FAIL, STATUS_CHOOSE_GAME, STATUS_GAME_SELECTED, \
    STATUS_POSITION_SHIPS, MSG_SEP, STATUS_USER_READY, NOTIFY

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

connected_players = []
active_games = []
channel.exchange_declare(exchange='logs',
                         type='fanout')

def send_toall(message):
    channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=str(NOTIFY) + message)
    print(" [x] Sent %r" % message)


class Player:
    def __init__(self, login):
        self.__login = str(login)
        self.__score = 0
        self.__ships = []

    def get_login(self):
        return self.__login

    def set_ships(self, ships):
        self.__ships = ships


class Game:
    def __init__(self, host):
        self.__host = host
        self.__players = []

    def get_host(self):
        return self.__host

    def change_host(self, host):
        self.__host = host

    def join_game(self, player):
        self.__players.append(player)

    def leave_game(self, player):
        for i in range(len(self.__players)):
            if self.__players[i].get_login() == player.get_login():
                self.__players.pop(i)

    def get_players(self):
        return self.__players


def prepare_list_of_active_games():
    i = 0
    result = str(i) + '. Host your game\n'
    for j in range(len(active_games)):
        i += 1
        result += str(i) + '. ' + active_games[j].get_host().get_login() + '\'s game\n'
    return result


def prepare_response(body):
    reqCode = int(body.split(MSG_SEP)[0])
    request = body.split(MSG_SEP)[1]
    # print str(reqCode)
    if reqCode == STATUS_CONNECTED:
        for i in range(len(connected_players)):
            if request == connected_players[i].get_login():
                return str(STATUS_LOGIN_FAIL) + MSG_SEP + 'This login already in use, try another one'
        connected_players.append(Player(request))
        return str(STATUS_CONNECTED) + MSG_SEP + 'Connected as ' + request
    elif reqCode == STATUS_EXIT:
        # player should also be removed from the game
        # if he hosts a game and wants to leave, then a new host should be chosen among the players
        # or the game session ends (game should be removed from active_games)
        for i in range(len(connected_players)):
            if request == connected_players[i].get_login():
                connected_players.pop(i)
        return str(STATUS_EXIT) + MSG_SEP + 'Exiting the game'
    elif reqCode == STATUS_CHOOSE_GAME:
        return str(STATUS_CHOOSE_GAME) + MSG_SEP + prepare_list_of_active_games()
    elif reqCode == STATUS_GAME_SELECTED:
        login = body.split(MSG_SEP)[2]
        player = None
        for i in range(len(connected_players)):
            if login == connected_players[i].get_login():
                player = connected_players[i]
        try:
            selected_game = int(request)
            if selected_game == 0:
                newGame = Game(player)
                active_games.append(newGame)
                msg = 'You have created a new game'
            else:
                # select a game to join by number (client entered numbers are shifted to the right,
                # as number 0 is 'host own game')
                game_to_join = active_games[selected_game - 1]
                game_to_join.join_game(player)
                #should notify the host and other players about new joining players
                msg = 'You have joined the game'
        except:
            return str(STATUS_CONNECTED) + MSG_SEP + 'Wrong value is entered'
        return str(STATUS_POSITION_SHIPS) + MSG_SEP + msg
    elif reqCode == STATUS_USER_READY:
        #print body
        login = body.split(MSG_SEP)[2]
        send_toall(login)
        return str(STATUS_POSITION_SHIPS) + MSG_SEP
    else:
        return None


def on_request(ch, method, props, body):
    response = prepare_response(body)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id, delivery_mode=2,),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()