from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from influxdb import InfluxDBClient


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graphic")
        self.setGeometry(100, 100, 700, 500)

        self.show()

        self.create_line_chart(self.choose_param())

    def connect(self, param):
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('Table')
        results = client.query('select * from sec')
        return results.get_points(tags={'param': param})

    def create_line_chart(self, param):
        series = QLineSeries()
        for point in self.connect(param):
            series.append(float(point['phase']), point['value'])

        chart = QChart()

        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Parameter " + param)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)

    def choose_param(self):
        print('Choose an parameter:')
        param = input()
        return param


App = QApplication(sys.argv)
w = Window()
sys.exit(App.exec_())
