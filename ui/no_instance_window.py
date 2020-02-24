from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QShortcut, QLabel, QVBoxLayout


class NoInstanceWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        self.parentWindow = mainWindow
        # Set the window properties
        self.setWindowTitle("Do you want to close the application?")
        self.setWindowIcon(QIcon('resources/logo.png'))
        self.setGeometry(300, 300, 600, 100)

        # Create the central widget
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        # Create the buttons used in the window
        self.create_buttons()

        # So that user can close this window by pressing the Escape key
        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.escape.activated.connect(self.close)

        self.create_layout()

    def create_buttons(self):
        self.create_instance_button = QPushButton("Create new Instance")
        self.create_instance_button.setDefault(True)
        self.create_instance_button.clicked.connect(self.create_instance)

        self.open_instance_button = QPushButton("Open existing Instance")
        self.open_instance_button.setAutoDefault(True)
        self.open_instance_button.clicked.connect(self.open_instance)

        self.setStyleSheet("QPushButton { background-color: maroon }")

    # |--------------------------------------|
    # |                                      |
    # |  No instance has been selected!      |
    # |                                      |
    # |       [CREATE] [OPEN]                |
    # |--------------------------------------|
    def create_layout(self):
        # The main layout the will contain all other layouts
        self.main_layout = QHBoxLayout(self.cw)

        # Putting the proper message on the application
        self.main_layout.addWidget(QLabel("No instance has been selected!!"))

        # The layout containing the Create and Open buttons
        self.buttons_layout = QVBoxLayout(self.cw)
        self.buttons_layout.addWidget(self.create_instance_button)
        self.buttons_layout.addWidget(self.open_instance_button)

        # Add the layout containing the buttons to the main layout
        self.main_layout.addLayout(self.buttons_layout)


    def create_instance(self):
        self.parentWindow.add_instance()
        self.close()

    def open_instance(self):
        self.parentWindow.open_instance()
        self.close()
