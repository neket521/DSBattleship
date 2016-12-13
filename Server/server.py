import pika
from common import STATUS_CONNECTED, STATUS_EXIT, STATUS_LOGIN_FAIL, STATUS_CHOOSE_GAME, STATUS_GAME_SELECTED, \
    STATUS_POSITION_SHIPS

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port = 5672))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

connected_players = []

class Player:

    def __init__(self, login):
        self.login = str(login)
        self.score = 0

    def get_login(self):
        return self.login

def prepare_list_of_active_games():
    return '0. Host your game\n1. bob\'s game'

def prepare_response(reqCode, request):
    #print str(reqCode)
    if reqCode == STATUS_CONNECTED:
        for i in range(len(connected_players)):
            if request == connected_players[i].get_login():
                return str(STATUS_LOGIN_FAIL)+':'+'This login already in use, try another one'
        connected_players.append(Player(request))
        #check if there are available games
        return str(STATUS_CONNECTED)+':'+'Connected as '+request
    elif reqCode == STATUS_EXIT:
        for i in range(len(connected_players)):
            if request == connected_players[i].get_login():
                connected_players.pop(i)
        return str(STATUS_EXIT)+':'+'Exiting the game'
    elif reqCode == STATUS_CHOOSE_GAME:
        return str(STATUS_CHOOSE_GAME)+':'+prepare_list_of_active_games()
    elif reqCode == STATUS_GAME_SELECTED:
        try:
            selected_game = int(request)
            if selected_game == 0:
                msg = 'You have hosted the game'
            else:
                msg = 'You have joined the game'
        except:
            return str(STATUS_CONNECTED)+':'+'Wrong value is entered'
        return str(STATUS_GAME_SELECTED)+':'+msg
    else:
        return None

def on_request(ch, method, props, body):
    reqCode = int(body.split(':')[0])
    request = body.split(':')[1]
    response = prepare_response(reqCode, request)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id,),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
