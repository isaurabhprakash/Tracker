# --------------------------------------------------------------------#
# Implements the code for the the Add Log Window. This window is      #
# opened when the user clicks on the "Add +" button.                  #
# --------------------------------------------------------------------#

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QShortcut, QLineEdit, QPushButton


class AddInstanceWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Hold the reference to the parent window
        self.parentWindow = mainWindow

        # Set the window properties
        self.setWindowTitle("Create a new Instance")
        self.setWindowIcon(QIcon('./resources/logo.png'))
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

        # Create the widget for taking the user input.
        self.create_lineedit()

        # Create the buttons that will be used in the window
        self.create_buttons()

        # The main layout. This layout will contain other children layouts.
        self.main_layout = QVBoxLayout(self.cw)

        # Create the top layout - Containing Name
        self.top_layout = QHBoxLayout(self.cw)
        self.top_layout.addWidget(QLabel('Name\t'))
        self.top_layout.addWidget(self.instanceLine)

        # Create the bottom layout that will eventually contain the Create button.
        self.bottom_layout = QHBoxLayout(self.cw)

        # This layout is created so that the Create button comes on the
        # right side of the window.
        self.empty_bottom_layout = QHBoxLayout()
        self.empty_bottom_layout.addStretch(3)

        # This layout will actually contain the Create buttons.
        self.right_bottom_layout = QHBoxLayout(self.cw)
        self.right_bottom_layout.addWidget(self.create_button)

        self.bottom_layout.addLayout(self.empty_bottom_layout)
        self.bottom_layout.addLayout(self.right_bottom_layout)

        # Add the children layouts to the main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.setStyleSheet("QPushButton { background-color: maroon }")
        self.setLayout(self.main_layout)

        # So the the window closes when the user presses the Esc key.
        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self.cw)
        self.escape.activated.connect(self.close)

    # ----------------------------------------------------------------#
    # Creates the QLinEdit widget used for taking the user input.     #
    # ----------------------------------------------------------------#
    def create_lineedit(self):
        self.instanceLine = QLineEdit(self.cw)
        self.instanceLine.returnPressed.connect(self.create_instance)

    # ----------------------------------------------------------------#
    # Creates the 'Create" button used in the app.                    #
    # ----------------------------------------------------------------#
    def create_buttons(self):
        self.create_button = QPushButton("Create", self.cw)
        self.create_button.clicked.connect(self.create_instance)

        # We want the instance to be created when the user presses enter.
        self.create_button.setShortcut(QKeySequence(Qt.Key_Return))

    # ----------------------------------------------------------------#
    # This function is called when the user clicks on the "Create"    #
    # button.                                                         #
    # ----------------------------------------------------------------#
    def create_instance(self):
        print("Create Clicked")
        text = self.instanceLine.text()

        # User has actually entered some name
        if text != '':
            self.parentWindow.create_new_instance(text)

        self.close()