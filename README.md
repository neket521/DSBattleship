# DSBattleship
Traditional rules are explained here: [link](https://en.wikipedia.org/wiki/Battleship_%28game%29). In our implementation, we will not limit the game to 2 players, but the multi-player option will be introduced (at least 3 players). We just assume that all the war-parties are fighting each other (aka “Deathmatch”). The winner is the last one standing on the sea battlefield. Optionally, we can score each successful hit.
Ships:
* Carrier of size 4     x1
* Battleship of size 3  x2
* Cruiser of size 2     x3
* Submarine of size 1   x4

## Prerequisites
### Pika
To install Pika simply use:
```
pip install pika
```
### RabbitMQ
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
