from influxdb import InfluxDBClient
from mqtt import Broker
from random import randint


class Param(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name


def conn():
    global client
    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('Table')
    client.switch_database('Table')


def get_point():
    results = client.query('select * from sec')
    return results.get_points()


def list_param():
    results = client.query('select * from sec')
    points = results.get_points()

    list_param = []
    params = ''
    for point in points:
        if point['param'] not in list_param:
            list_param.append(point['param'])
            params += point['param'] + '; '
    result = str(len(list_param)) + ": " + params
    print('Number of parameters = ', result + list_param[0])


def add_param():
    print('Enter name, frequency and initial value:')
    name, freq, value = input().split()

    p = Param(name, int(value))

    list_param = {}

    for param in range(5):
        param = 'num' + str(param)
        if param not in list_param:
            p = Param(param, randint(0, 100))
            list_param[p.get_name()] = p.get_value()
    print(list_param)

    list_param[p.name] = p.value


if __name__ == "__main__":
    conn()
    br = Broker()

    while True:
        print('Choose an action (add, list, stop)')
        act = input().strip()

        if act == 'add':
            add_param()
        elif act == 'list':
            list_param()
        elif act == 'stop':
            break
        else:
            print('Unknown action')
            break

    """
    for point in conn():
        print("Time: %s, param: %s, phase: %s, value: %i" % (point['time'], point['param'], point['phase'], point['value']))
    """
