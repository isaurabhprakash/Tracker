from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget


class CloseWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Set the window properties
        self.setWindowTitle("Create a new Instance")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(300, 300, 600, 100)