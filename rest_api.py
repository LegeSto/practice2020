import flask
from flask import request, jsonify, render_template
from influxdb import InfluxDBClient
from datetime import datetime
from file import add_param_in_list


app = flask.Flask(__name__)


def db_connect():
    global points, client
    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('Table')
    client.switch_database('Table')
    results = client.query('select * from sec')
    points = results.get_points()


def init_books():
    global books
    books = []
    count = 0

    for point in points:
        point['id'] = count
        count += 1
        books.append("Time: %s, param: %s, phase: %s, value: %i" % \
                     (point['time'], point['param'], point['phase'], point['value']))


def reading_time(param):
    time_run = datetime.now()
    results = client.query('select ' + param + ' from sec')
    print('select ' + param + ' from sec')
    points_time = results.get_points()
    read_time = datetime.now() - time_run
    return str(read_time)


db_connect()
init_books()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Database InfuxDB</h1><p>This site is a prototype API.</p>"


@app.route('/resources/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/resources/read_time', methods=['POST', 'GET'])
def read_time():
    if request.method == 'POST':
        param = request.form['var']
        print(param)
        return reading_time(str(param))
    else:
        return render_template('read_time.html')


@app.errorhandler(404)
def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/resources', methods=['GET'])
def api_list():
    cnt = 0
    memory = ''

    for point in points:
        if point['param'] != memory:
            cnt += 1
            print("Param: %s" % (point['param']), end=', ')
            memory = point['param']
    result = 'Number of parameters:' + str(cnt)

    return jsonify(result)


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
        if book[{'tags': query}] == que:
            result.append(book)

    return jsonify(result)


@app.route('/add_param', methods=['POST', 'GET'])
def new_num():
    if request.method == 'POST':
        name = request.form['var']
        value = request.form['val']
        add_param_in_list(name, value)

    else:
        return render_template('add_param.html')


if __name__ == "__main__":

    app.run()
