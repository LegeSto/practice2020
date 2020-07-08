import flask
from flask import request, jsonify
from influxdb import InfluxDBClient

app = flask.Flask(__name__)
app.config["DEBUG"] = True

client = InfluxDBClient(host='localhost', port=8086)
client.create_database('Table')
client.switch_database('Table')
results = client.query('select * from sec')
points = results.get_points()
books = []
for point in points:
    books.append(point)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Database InfuxDB</h1><p>This site is a prototype API.</p>"


@app.route('/resources', methods=['GET'])
def api_all():
    return jsonify(books)


app.run()
