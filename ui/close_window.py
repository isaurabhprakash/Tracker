from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QShortcut, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel


class CloseWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Set the window properties
        self.setWindowTitle("Create a new Instance")
        self.setWindowIcon(QIcon('resources/logo.png'))
        self.setGeometry(300, 300, 600, 100)

        # Create the central widget
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        # Create the buttons used in the window
        self.create_buttons()

        # So that user can close this window by pressing the Escape key
        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.escape.activated.connect(self.close_window)

        self.create_layout()

    # |-----------------------------------------------------------|
    # |                                                           |
    # |          Are you sure you want to exit?                   |
    # |                                                           |
    # |                     [Save and Exit][Exit without Saving]  |
    # |-----------------------------------------------------------|

    def create_layout(self):
        # The main layout containing all other children layouts
        self.main_layout = QVBoxLayout(self.cw)

        self.main_layout.addWidget(QLabel("Are you sure you want to exit?"))

        # Create the bottom layout containing the buttons
        self.bottom_layout = QHBoxLayout(self.cw)
        self.bottom_layout.addLayout(QGridLayout())
        self.bottom_layout.addWidget(self.save_and_exit_button)
        self.bottom_layout.addWidget(self.force_exit_button)

        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)

    def create_buttons(self):
        self.save_and_exit_button = QPushButton("Save and exit")
        self.save_and_exit_button.setAutoDefault(True)
        self.force_exit_button = QPushButton("Don't Save")

        self.setStyleSheet("QPushButton { background-color: maroon }")

    def close_window(self):
        print("Cancel button pressed")
        self.close()
