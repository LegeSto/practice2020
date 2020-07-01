from influxdb import InfluxDBClient, resultset
import datetime
from time import sleep
from random import randint

client = InfluxDBClient(host='localhost', port=8086)
client.create_database('Table')
print(client.get_list_database())
client.switch_database('Table')

json_body = []

for i in range(10):
    s = {
        "measurement": "sec",
        "tags": {
            "param": i,
            "times": datetime.datetime.now()
        },
        "fields": {
            "value": int(randint(0, 100))
        }
    }
    sleep(1)
    json_body.append(s)

client.write_points(json_body)
results = client.query('select * from sec')
points = results.get_points()

for point in points:
    print("Time: %s, value: %i" % (point['times'], point['value']))

