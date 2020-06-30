from influxdb import InfluxDBClient
import json
import datetime
from random import randint

client = InfluxDBClient(host='localhost', port=8086)

client.create_database('Table')
print(client.get_list_database())
json_body = [
    {
        "measurement": "sec",
        "fields": {
            "value": randint(0, 10)
        }
    }
]

client.write_points(json_body)
