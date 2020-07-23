import flask
from flask import request, jsonify, render_template
from influxdb import InfluxDBClient
from datetime import datetime
import threading
from time import sleep
from random import randint
from mqtt import Broker
from bd import Param


def add_param_in_list(key, value):
    list_param[key] = value


def thread_function():
    global list_param, client

    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('Table')
    print(client.get_list_database())
    client.switch_database('Table')

    list_param = {}

    for param in range(5):
        param = 'num' + str(param)
        if param not in list_param:
            p = Param(param, randint(0, 100))
            list_param[p.get_name()] = p.get_value()
    print(list_param)
    br = Broker()
    phase = 0

    while True:
        for key in list_param:
            if key not in list_param:
                p = Param(key, randint(0, 100))
                add_param_in_list(p.get_name(), p.get_value())

            s = [{
                "measurement": "sec",
                "tags": {
                    "param": key,
                    "phase": phase,
                    "broker": br.broker_address,
                    "topic": br.topic
                },
                "fields": {
                    "value": list_param[key]
                }
            }]

            list_param[key] += randint(-2, 2)
            client.write_points(s)
        phase += 2
        sleep(2)


app = flask.Flask(__name__)


def db_connect():
    global client
    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('Table')
    client.switch_database('Table')


def init_books():
    global books
    books = []
    count = 0
    results = client.query('select * from sec')
    points = results.get_points()
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
    if 'id' in request.args:
        que = int(request.args['id'])
        query = 'id'
        result = []
        for book in books:
            if book[query] == que:
                result.append(book)
        return jsonify(result)
    else:
        results = client.query('select * from sec')
        points = results.get_points()

        list_param = []
        params = ''
        for point in points:
            if point['param'] not in list_param:
                list_param.append(point['param'])
                params += point['param'] + '; '
        result = 'Number of parameters = ' + str(len(list_param)) + ": " + params

        return jsonify(result)


@app.route('/add_param', methods=['POST', 'GET'])
def new_num():
    if request.method == 'POST':
        name = request.form['var']
        value = request.form['val']
        add_param_in_list(name, value)
        result = ''
        for i in list_param:
            result += str(i)
        return jsonify(result)
    else:
        return render_template('add_param.html')


if __name__ == "__main__":

    x = threading.Thread(target=thread_function)
    x.start()

    db_connect()
    init_books()

    app.run()
