from influxdb import InfluxDBClient, resultset
import datetime
from time import sleep
from random import randint

client = InfluxDBClient(host='localhost', port=8086)
client.create_database('Table')
print(client.get_list_database())
client.switch_database('Table')

json_body = []

for param in range(10):
    for i in range(5):
        s = {
            "measurement": "sec",
            "tags": {
                "param": param,
                "phase": i
            },
            "fields": {
                "value": param + i
            }
        }
        # sleep(0.1)
        json_body.append(s)

client.write_points(json_body)
results = client.query('select * from sec')
points = results.get_points()

for point in points:
    print("Time: %s, param: %s, phase: %s, value: %i" % (point['time'], point['param'], point['phase'],  point['value']))
