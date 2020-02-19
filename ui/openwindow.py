import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QListWidget, QLineEdit, QLabel, QVBoxLayout, QShortcut, QWidget, \
    QMainWindow


class InstanceSelectionWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Set the window properties
        self.setWindowTitle("Open Tracker Log")
        self.setWindowIcon(QIcon('./resources/logo.png'))
        self.setGeometry(300, 300, 600, 100)

        # Create the central widget
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        # Create the buttons in the layout
        self.create_buttons()

        # Now create the actual window
        self.create_layout()

        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self.cw)
        self.escape.activated.connect(self.close_window)

    # |----------------------------------------------------------------|
    # |                                                                |
    # |   Location :   [........................]  [ChangeLocation]    |
    # |                                                                |
    # |                 [------------------------]                     |
    # |                 [------------------------]                     |
    # |                 [------------------------]                     |
    # |                 [   Scrollable Area      ]                     |
    # |                 [------------------------]                     |
    # |                 [------------------------]                     |
    # |                 [------------------------]                     |
    # |                                             [Open]             |
    # |----------------------------------------------------------------|
    def create_layout(self):
        # The main layout that contains all the other layouts
        self.main_layout = QVBoxLayout(self.cw)

        # Create the upper layout containing Location and Location Selector icon
        self.upper_layout = QHBoxLayout()
        self.upper_layout.addWidget(QLabel('Location'))
        self.upper_layout.addWidget(QLineEdit('saurabh.trkr'))

        self.openIconButton = QPushButton()
        self.openIconButton.setIcon(QIcon('./resources/open.png'))

        self.upper_layout.addWidget(self.openIconButton)

        # Create the list widget containing the list of instances
        self.listWidget = QListWidget()
        self.listWidget.setFocus(Qt.OtherFocusReason)
        self.add_items_to_open_list()

        # Create the bottom layout containing the Open Log button
        self.bottom_layout = QHBoxLayout(self.cw)
        self.bottom_layout.addLayout(QHBoxLayout())
        self.bottom_layout.addWidget(self.openLog_button)

        # Add all the children layout to the main layout
        self.main_layout.addLayout(self.upper_layout)
        self.main_layout.addWidget(self.listWidget)
        self.listWidget.setFocus(Qt.OtherFocusReason)
        self.main_layout.addLayout(self.bottom_layout)

        self.cw.setLayout(self.main_layout)

    def create_buttons(self):
        self.openLog_button = QPushButton('Open Log')
        self.openLog_button.setStyleSheet("background-color : maroon")
        self.openLog_button.setShortcut(QKeySequence(Qt.Key_Return))

    def add_items_to_open_list(self):
        self.listWidget.clear()
        instanceList = os.listdir('./logs/')
        instanceList.sort()
        for name in instanceList:
            if os.path.isfile(os.path.join('./logs/', name)) and name != "trkr":
                self.listWidget.addItem(name)

    def close_window(self):
        print('Escape Pressed')
        self.close()
