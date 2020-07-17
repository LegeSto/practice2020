import paho.mqtt.client as mqtt
from time import sleep


def on_log(client, userdata, level, buf):
    print('log: ' + buf)


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('connect OK')
    else:
        print('Bad connection Returned code=', rc)
    client.subscribe("/#")


broker = 'localhost'

client = mqtt.Client('Cl1')
client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message
print('Connecting to broker', broker)
client.connect(broker)

client.loop_forever()
