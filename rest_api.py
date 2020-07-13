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
count = 0
for point in points:
    point['id'] = count
    count += 1
    books.append(point)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Database InfuxDB</h1><p>This site is a prototype API.</p>"


@app.route('/resources/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/resources', methods=['GET'])
def api_filter():
    if 'id' in request.args:
        que = int(request.args['id'])
        query = 'id'
    elif 'param' in request.args:
        que = int(request.args['param'])
        query = 'param'
    else:
        return "Error: No id field provided. Please specify an id."

    result = []

    for book in books:
        if book[query] == que:
            result.append(book)

    return jsonify(result)


app.run()
