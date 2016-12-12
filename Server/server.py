import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port = 5672))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue_durable', durable = True)


class Player:
    def __init__(self, login):
        self.login = login
        self.score = 0


def on_request(ch, method, props, body):
    request = str(body)

    #response =

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id,
                                                     delivery_mode=2,),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue_durable')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
