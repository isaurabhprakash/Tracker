from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QShortcut, QLineEdit, QPushButton

import __main__
from __main__ import *


class AddInstanceWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Set the window properties
        self.setWindowTitle("Create a new Instance")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(300, 300, 600, 100)

        # Create the central widget
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        # Now create the central widget
        # |----------------------------------------|
        # |                                        |
        # |   Name :   [....................]      |
        # |                                        |
        # |                 [CREATE]   [Cancel]    |
        # |----------------------------------------|

        # Create the buttons that will be used in the window
        self.create_lineedit()
        self.create_buttons()

        self.main_layout = QVBoxLayout(self.cw)

        # Create the upper layout - Containing Name
        self.upper_layout = QHBoxLayout(self.cw)
        self.upper_layout.addWidget(QLabel('Name\t'))
        self.upper_layout.addWidget(self.instanceLine)

        # Create the layout containing Create and Cancel buttons
        self.lower_layout = QHBoxLayout(self.cw)

        self.empty_lower_layout = QHBoxLayout()
        self.empty_lower_layout.addStretch(3)

        self.right_lower_layout = QHBoxLayout(self.cw)
        self.right_lower_layout.addWidget(self.create_button)

        self.lower_layout.addLayout(self.empty_lower_layout)
        self.lower_layout.addLayout(self.right_lower_layout)

        # Add the children layouts to the main layout
        self.main_layout.addLayout(self.upper_layout)
        self.main_layout.addLayout(self.lower_layout)
        self.setStyleSheet("QPushButton { background-color: maroon }")
        self.setLayout(self.main_layout)

        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self.cw)
        self.escape.activated.connect(self.close_window)

    def create_lineedit(self):
        self.instanceLine = QLineEdit(self.cw)
        self.instanceLine.returnPressed.connect(self.create_instance)

    def create_buttons(self):
        self.create_button = QPushButton("Create", self.cw)
        self.create_button.clicked.connect(self.create_instance)
        self.create_button.setShortcut(QKeySequence(Qt.Key_Return))

    def create_instance(self):
        print("Create Clicked")
        text = self.instanceLine.text()
        __main__.window.create_new_instance(text)

    def close_window(self):
        print("Cancel button pressed")
        self.close()