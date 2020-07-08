from influxdb import InfluxDBClient
from time import sleep
from random import randint


class Param():
    def __init__(self, name, freq, value):
        self.name = name
        self.freq = freq
        self.value = value


def conn():
    results = client.query('select * from sec')
    return results.get_points()


def list_param(points):
    count = 0
    memory = ''

    for point in conn():
        if point['param'] != memory:
            count += 1
            print("Param: %s" % (point['param']), end=', ')
            memory = point['param']

    print()
    print('Number of parameters:', count)


def add_param():
    print('Enter name, frequency and initial value:')
    name, freq, value = input().split()
    print('Wait...')

    p = Param(name, float(freq), int(value))
    phase = 0

    while phase <= 10:
        s = [{
                "measurement": "sec",
                "tags": {
                    "param": p.name,
                    "phase": phase,
                    "freq": p.freq
                },
                "fields": {
                    "value": p.value
                }
            }]

        p.value += randint(-1, 1)
        phase += p.freq
        sleep(p.freq)
        client.write_points(s)


client = InfluxDBClient(host='localhost', port=8086)
client.create_database('Table')
client.switch_database('Table')

stop = True

while stop:
    print('Choose an action (add, list, stop)')
    act = input().strip()

    if act == 'add':
        add_param()
    elif act == 'list':
        list_param(conn())
    elif act == 'stop':
        stop = False
    else:
        print('Unknown action')
        stop = False

"""
for point in conn():
    print("Time: %s, param: %s, phase: %s, value: %i" % (point['time'], point['param'], point['phase'], point['value']))
"""