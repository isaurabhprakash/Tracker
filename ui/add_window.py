# --------------------------------------------------------------------#
# Implements the code for the the Add Log Window. This window is      #
# opened when the user clicks on the "Add +" button.                  #
# --------------------------------------------------------------------#

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QShortcut, QLineEdit, QPushButton, \
    QSpinBox, QMessageBox


class AddInstanceWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Hold the reference to the parent window
        self.parentWindow = mainWindow

        # Set the window properties
        self.set_window_properties()

        # Create widgets used in the window
        self.create_widgets()

        # Create the layout for the window
        self.create_layout()

        # So the the window closes when the user presses the Esc key.
        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self.cw)
        self.escape.activated.connect(self.close)

    def set_window_properties(self):
        self.setWindowTitle("Create a new Instance")
        self.setWindowIcon(QIcon('./resources/logo.png'))
        self.setGeometry(300, 300, 600, 100)

    def create_widgets(self):
        # Create the widget for taking the user input.
        self.create_lineedit()

        # Create spin boxes
        self.create_spinBoxes()

        # Create the "Create" button
        self.create_buttons()

    # ----------------------------------------------------------------#
    # Creates the QLinEdit widget used for taking the user input.     #
    # ----------------------------------------------------------------#
    def create_lineedit(self):
        # Create the central widget. Everything will be created on top of this.
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        # Line to take the instance name
        self.instanceLine = QLineEdit(self.cw)
        self.instanceLine.returnPressed.connect(self.create_instance)

        # Line to take the unit Name
        self.unitLine = QLineEdit(self.cw)

    def create_spinBoxes(self):
        self.fromRangeBox = QSpinBox(self.cw)
        self.toRangeBox = QSpinBox(self.cw)

        self.fromRangeBox.setValue(60)
        self.toRangeBox.setValue(120)

    # ----------------------------------------------------------------#
    # Creates the 'Create" button used in the app.                    #
    # ----------------------------------------------------------------#
    def create_buttons(self):
        self.create_button = QPushButton("Create", self.cw)
        self.create_button.clicked.connect(self.create_instance)

        # We want the instance to be created when the user presses enter.
        self.create_button.setShortcut(QKeySequence(Qt.Key_Return))

    # |---------------------------------------------|
    # |                                             |
    # |   Name :   [....................]           |
    # |   Unit :   [...]   Range: [...] to [...]    |
    # |                                             |
    # |                                    [CREATE] |
    # |---------------------------------------------|
    def create_layout(self):
        # The main layout. This layout will contain other children layouts.
        self.main_layout = QVBoxLayout(self.cw)

        # Create the top layout - Containing Name
        self.name_layout = QHBoxLayout(self.cw)
        self.name_layout.addWidget(QLabel('Name\t'))
        self.name_layout.addWidget(self.instanceLine)

        # Create the center layout - Containing unit
        self.rangeunit_layout = QHBoxLayout(self.cw)
        self.rangeunit_layout.addWidget(QLabel('Unit\t'))
        self.rangeunit_layout.addWidget(self.unitLine)
        self.rangeunit_layout.addWidget(QLabel("Range"))
        self.rangeunit_layout.addWidget(self.fromRangeBox)
        self.rangeunit_layout.addWidget(QLabel("to"))
        self.rangeunit_layout.addWidget(self.toRangeBox)

        # Create the bottom layout that will eventually contain the Create button.
        self.button_layout = QHBoxLayout(self.cw)

        # This layout is created so that the Create button comes on the
        # right side of the window.
        self.empty_button_layout = QHBoxLayout()
        self.empty_button_layout.addStretch(3)

        # This layout will actually contain the Create buttons.
        self.right_button_layout = QHBoxLayout(self.cw)
        self.right_button_layout.addWidget(self.create_button)

        self.button_layout.addLayout(self.empty_button_layout)
        self.button_layout.addLayout(self.right_button_layout)

        # Add the children layouts to the main layout
        self.main_layout.addLayout(self.name_layout)
        self.main_layout.addLayout(self.rangeunit_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setStyleSheet("QPushButton { background-color: maroon }")
        self.setLayout(self.main_layout)

    # ----------------------------------------------------------------#
    # This function is called when the user clicks on the "Create"    #
    # button.                                                         #
    # ----------------------------------------------------------------#
    def create_instance(self):
        print("Create Clicked")
        instance_name = self.instanceLine.text()
        unit_name = self.unitLine.text()
        from_range = self.fromRangeBox.value()
        to_range = self.toRangeBox.value()

        if instance_name == '' or unit_name == '':
            self.msg = QMessageBox()
            self.msg.setWindowIcon(QIcon('resources/logo.png'))
            self.msg.setGeometry(300, 300, 600, 100)
            self.msg.setWindowTitle("Oops!!")

            if instance_name == '' and unit_name == '':
                self.msg.setText("Neither instance name nor unit name can be blank!")
            else:
                if instance_name == '':
                    self.msg.setText("Instance name can not be blank!")
                else:
                    self.msg.setText("Unit name can not be blank!")

            self.msg.show()
        else:
            self.parentWindow.create_new_instance(instance_name, unit_name, from_range, to_range)
            self.close()
