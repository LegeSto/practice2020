from PyQt5 import Qt
import pyqtgraph as pg
from influxdb import InfluxDBClient


class Window(Qt.QWidget):

    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout(self)

        self.view = view = pg.PlotWidget()
        self.curve = view.plot(name="Line")

        self.btn = Qt.QPushButton("Plot")
        self.btn.clicked.connect(self.plot)

        layout.addWidget(Qt.QLabel("Graphic"))
        layout.addWidget(self.view)
        layout.addWidget(self.btn)

    def plot(self):
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('Table')
        results = client.query('select * from sec')
        points = results.get_points()    # tags={'param': '1'}
        array = []
        for point in points:
            array.append(point['value'])
        self.curve.setData(array)


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
