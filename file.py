from influxdb import InfluxDBClient
from time import sleep
from random import randint

client = InfluxDBClient(host='localhost', port=8086)
client.create_database('Table')
print(client.get_list_database())
client.switch_database('Table')

json_body = []

for param in range(5):
    phase = 0
    freq = randint(1, 5)
    value = randint(0, 50)
    while phase <= 9:
        s = {
            "measurement": "sec",
            "tags": {
                "param": str(param),
                "phase": phase,
                "freq": freq
            },
            "fields": {
                "value": value
            }
        }
        value += randint(-1, 1)
        phase += freq
        sleep(freq)
        json_body.append(s)

client.write_points(json_body)
results = client.query('select * from sec')
points = results.get_points()

for point in points:
    print("Time: %s, param: %s, phase: %s, value: %i" % (point['time'], point['param'], point['phase'],  point['value']))
