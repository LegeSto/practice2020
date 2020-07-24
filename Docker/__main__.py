from influxdb import InfluxDBClient
import threading
from time import sleep
from random import randint
from mqtt import Broker
from bd import Param
import rest_api as API


def add_param_in_list(key, value):
    list_param[key] = value


def thread_function():
    global points, list_param, client

    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('Table')
    print(client.get_list_database())
    client.switch_database('Table')

    list_param = {}

    for param in range(5):
        param = 'num' + str(param)
        if param not in list_param:
            p = Param(param, randint(0, 100))
            list_param[p.get_name()] = p.get_value()
    print(list_param)
    br = Broker()
    phase = 0

    while True:
        for key in list_param:
            if key not in list_param:
                p = Param(key, randint(0, 100))
                add_param_in_list(p.get_name(), p.get_value())

            s = [{
                "measurement": "sec",
                "tags": {
                    "param": key,
                    "phase": phase,
                    "broker": br.broker_address,
                    "topic": br.topic
                },
                "fields": {
                    "value": list_param[key]
                }
            }]

            list_param[key] += randint(-2, 2)
            client.write_points(s)
        phase += 2
        sleep(2)


if __name__ == "__main__":

    x = threading.Thread(target=thread_function)
    x.start()

    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('Table')
    print(client.get_list_database())
    client.switch_database('Table')
    results = client.query('select * from sec')
    points = results.get_points()
    for point in points:
        print("Time: %s, param: %s, phase: %s, value: %i" % \
              (point['time'], point['param'], point['phase'], point['value']))

    API.app.run()

'''
    graf.graph()
'''