# DSBattleship
Rules to be described (deathmatch, how many ships of what size). Detailed rules explained by the link (link to wikipedia).

## Prerequisites
* Pika
To install Pika simply use:
```
pip install pika
```
* RabbitMQ
To install RabbitMQ go to the [download page](https://www.rabbitmq.com/download.html) and choose a suitable for your OS version.

On Ubuntu you might want to also install RabbitMQ Management Console:
```
sudo rabbitmq-plugins enable rabbitmq_management
```
Once you've enabled the console, it can be accessed using your favourite web browser by visiting: 
```
http://[your droplet's IP]:15672/.
```
The default username and password are both set “guest” for the log in.

Managing RabbitMQ on Ubuntu:
```
# To start the service:
service rabbitmq-server start

# To stop the service:
service rabbitmq-server stop

# To restart the service:
service rabbitmq-server restart

# To check the status:
service rabbitmq-server status
```
