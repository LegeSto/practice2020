from influxdb import InfluxDBClient
from time import sleep
from random import randint
from mqtt import Broker

client = InfluxDBClient(host='localhost', port=8086)
client.create_database('Table')
print(client.get_list_database())
client.switch_database('Table')

br = Broker()
json_body = []

for param in range(5):
    phase = 0
    freq = randint(1, 5)
    value = randint(0, 50)
    while phase <= 9:
        s = [{
            "measurement": "sec",
            "tags": {
                "param": str(param),
                "phase": phase,
                "freq": freq,
                "broker": br.broker_address,
                "topic": br.topic
            },
            "fields": {
                "value": value
            }
        }]
        value += randint(-1, 1)
        phase += freq
        sleep(freq)
        client.write_points(s)

results = client.query('select * from sec')
points = results.get_points()

for point in points:
    print("Time: %s, param: %s, phase: %s, value: %i" % (point['time'], point['param'], point['phase'], point['value']))
