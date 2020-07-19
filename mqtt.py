import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from time import sleep


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
    client.publish(br.topic, "On")
    sleep(5)
    client.loop_stop()
    # client.loop_forever()
