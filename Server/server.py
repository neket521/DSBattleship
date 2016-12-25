import pika
from common import STATUS_CONNECTED, STATUS_EXIT, STATUS_LOGIN_FAIL, STATUS_CHOOSE_GAME, STATUS_GAME_SELECTED, \
    STATUS_POSITION_SHIPS, MSG_SEP, STATUS_USER_READY, NOTIFY_READY, NOTIFY_JOINED, GAME_STARTED, STATUS_SHOOTING, \
    STATUS_WAITING, NOTIFY_ALL_READY

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

connected_players = []
active_games = []
channel.exchange_declare(exchange='notifications', type='fanout')

def send_toall(code, message):
    body_to_send = str(code) + MSG_SEP + message
    channel.basic_publish(exchange='notifications',
                      routing_key='',
                      body=body_to_send)


class Player:
    def __init__(self, login):
        self.__login = str(login)
        self.__score = 0
        self.__is_ready = False

    def get_login(self):
        return self.__login

    def set_player_ready(self, is_ready):
        self.__is_ready = is_ready

    def is_ready(self):
        return self.__is_ready


class Game:
    def __init__(self, host):
        self.__host = host
        self.__players = []
        self.__players.append(host)

    def get_host(self):
        return self.__host

    def get_player_count(self):
        return len(self.__players)

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

    def set_is_ready(self, login, is_ready):
        for i in range(len(self.__players)):
            if self.__players[i].get_login() == login:
                self.__players[i].set_player_ready(is_ready)

    def all_players_ready(self):
        if len(self.__players) < 2:
            return False
        for player in self.__players:
            if not player.is_ready():
                return False
        return True


def prepare_list_of_active_games():
    i = 0
    result = str(i) + '. Host your game\n'
    for j in range(len(active_games)):
        i += 1
        result += str(i) + '. ' + active_games[j].get_host().get_login() + '\'s game\n'
    return result

def get_game_by_host(login):
    for j in range(len(active_games)):
        if active_games[j].get_host().get_login() == login:
            return active_games[j]

def prepare_response(body):
    reqCode = int(body.split(MSG_SEP)[0])
    request = body.split(MSG_SEP)[1]
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
                if game_to_join.all_players_ready():
                    return str(STATUS_CONNECTED) + MSG_SEP + 'Cannot join. Game in progress'
                else:
                    game_to_join.join_game(player)
                    send_toall(NOTIFY_JOINED, player.get_login())
                    msg = 'You have joined the game'
        except:
            return str(STATUS_CONNECTED) + MSG_SEP + 'Wrong value is entered'
        return str(STATUS_POSITION_SHIPS) + MSG_SEP + msg
    elif reqCode == STATUS_USER_READY:
        game_index = int(body.split(MSG_SEP)[1])
        login = body.split(MSG_SEP)[2]
        if game_index == 0:
            selected_game = get_game_by_host(login)
        else:
            selected_game = active_games[game_index - 1]
        selected_game.set_is_ready(login, True)
        send_toall(NOTIFY_READY, login)
        # if all users in this game are ready, start shooting
        if selected_game.all_players_ready():
            send_toall(NOTIFY_ALL_READY, selected_game.get_players()[0].get_login())
            return str(STATUS_SHOOTING) + MSG_SEP + selected_game.get_players()[0].get_login()
        else:
            return str(STATUS_WAITING) + MSG_SEP
    else:
        return str(STATUS_EXIT) + + MSG_SEP + 'Something went wrong. Exiting...'


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