from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QShortcut, QDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class GraphWindow(QDialog):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Hold the reference to the parent window
        self.parentWindow = mainWindow

        # Set the window properties
        self.setWindowTitle("Graph of your data")
        self.setWindowIcon(QIcon('./resources/logo.png'))
        # self.setGeometry(300, 300, 600, 100)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # So the the window closes when the user presses the Esc key.
        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.escape.activated.connect(self.close)

        self.plot_graph()

    def plot_graph(self):
        day_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        weight_list = [11, 12, 23, 44, 15, 36, 67, 87, 559, 410, 211, 12, 13, 15, 5, 1, 177, 58, 69, 50]

        self.parentWindow.slider.setMinimum(0)
        self.parentWindow.slider.setMaximum(6)
        self.parentWindow.slider.setValue(2)
        self.parentWindow.slider.setTickPosition(2)
        self.parentWindow.slider.setSingleStep(1)

        # create an axis
        #ax = self.figure.add_subplot(111)

        plt.xlabel("Days")
        plt.ylabel("Weight (in Kg)")
        plt.title("Weight Monitoring")

        plt.plot(day_list, weight_list, color='orange', marker='o',
                 markerfacecolor='red')

        # plot data
        #ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
