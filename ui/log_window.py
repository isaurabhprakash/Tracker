from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget, QShortcut


class LogWindow(QMainWindow):
    def __init__(self, mainWindow, pRows, pColumns, pUnitName):
        QWidget.__init__(self)

        self.parentWindow = mainWindow
        if pRows > 20:
            self.rows = pRows
        else:
            self.rows = 20  # Looks good :P

        self.columns = pColumns
        self.unitName = pUnitName

        # Set the window properties
        self.set_window_properties()

        # Create the central widget
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        # Create the widgets
        self.create_widgets()

        # Create the layouts
        self.create_layout()

        # So that user can close this window by pressing the Escape key
        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.escape.activated.connect(self.close)

    def set_window_properties(self):
        self.setWindowTitle("Logs")
        self.setWindowIcon(QIcon('resources/logo.png'))
        self.setGeometry(600, 50, 400, 680)
        self.setMinimumWidth(300)

    def create_layout(self):
        self.mainLayout = QVBoxLayout(self.cw)
        self.menuLayout = QHBoxLayout(self.cw)

        self.menuLayout.addWidget(QLabel("Menu"))

        self.dataLayout = QVBoxLayout(self.cw)
        self.dataLayout.addWidget(self.dataArea)
        self.dataLayout.stretch(1)

        self.mainLayout.addLayout(self.menuLayout)
        self.mainLayout.addLayout(self.dataLayout)

    def create_widgets(self):
        self.dataArea = QTableWidget(self.rows, self.columns)
        self.dataArea.horizontalHeader().setStretchLastSection(True)
        self.dataArea.verticalHeader().setStretchLastSection(True)
        headings = ["Date", self.parentWindow.currentInstanceName]
        self.dataArea.setHorizontalHeaderLabels(headings)
