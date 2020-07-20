import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from time import sleep
from random import randint


class Broker(object):
    def __init__(self):
        self.broker_address = "localhost"
        self.port = "1883"
        self.client = "Cl1"
        self.topic = "InfluxDB"


def conn():
    global cl
    cl = InfluxDBClient(host='localhost', port=8086)
    cl.create_database('Table')
    cl.switch_database('Table')


def add_param():
    print('Enter name, frequency and initial value:')
    name, freq, value = input().split()
    freq, value = float(freq), int(value)
    print('Wait...')
    p = ("Param: %s, frequency: %f, initial value: %i" % (name, freq, value))
    phase = 0

    while phase <= 10:
        s = [{
                "measurement": "sec",
                "tags": {
                    "param": name,
                    "phase": phase,
                    "freq": freq,
                    "broker": br.broker_address,
                    "topic": br.topic
                },
                "fields": {
                    "value": int(value)
                }
            }]

        value += randint(-1, 1)
        phase += freq
        sleep(freq)
        cl.write_points(s)
    return p


def get_point():
    results = cl.query('select * from sec')
    return results.get_points()


def on_message(client, userdata, message):
    print("topic:", message.topic)
    print("qos =", message.qos, "retain flag =", message.retain)
    print("message:", str(message.payload.decode("utf-8")))


def on_log(client, userdata, level, buf):
    print("log:", buf)


def mess():
    res = ''
    for point in get_point():
        for p in point:
            res += p + ': ' + str(point[p]) + ', '
        res += '\n'
    return res


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('connect OK')
    else:
        print('Bad connection Returned code=', rc)
    client.subscribe("#")


def publish_message():
    print("Choose an action (add_param) or write a massage")
    text = input()
    if text.lower() == 'add_param':
        text += add_param()
    return text


if __name__ == "__main__":
    conn()
    br = Broker()

    print("creating new instance")
    client = mqtt.Client(br.client)

    client.on_message = on_message
    client.on_log = on_log
    client.on_connect = on_connect

    print('Connecting to broker', br.broker_address)
    client.connect(br.broker_address)
    client.loop_start()
    client.publish(br.topic, publish_message())
    sleep(5)
    client.loop_stop()
    # client.loop_forever()
