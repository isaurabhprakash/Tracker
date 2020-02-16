from PyQt5.QtCore import Qt, QDate, pyqtSignal
from datetime import datetime
from PyQt5.QtWidgets import QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QCalendarWidget, \
    QSlider, QDoubleSpinBox, QMainWindow, QShortcut, QFileDialog, QScrollArea, QGroupBox, QFormLayout, QListWidget
from PyQt5.QtGui import QPalette, QColor, QIcon, QFont, QKeySequence

from database.datafile import *


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
        print("Instance created")

    def close_window(self):
        print("Cancel button pressed")
        self.close()


class InstanceSelectionWindow(QMainWindow):
    def __init__(self, mainWindow):
        QWidget.__init__(self)

        # Set the window properties
        self.setWindowTitle("Open Tracker Log")
        self.setWindowIcon(QIcon('logo.png'))
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
        self.openIconButton.setIcon(QIcon('open.png'))

        self.upper_layout.addWidget(self.openIconButton)

        # Create the list widget containing the list of instances
        self.listWidget = QListWidget()
        self.listWidget.setFocus(Qt.OtherFocusReason)
        #self.listWidget.setFixedHeight(200)
        self.listWidget.addItem("Saurabh")
        self.listWidget.addItem("Prakash")
        self.listWidget.addItem("Item3")
        self.listWidget.addItem("Item4")
        self.listWidget.addItem("Item5")
        self.listWidget.addItem("Item6")
        self.listWidget.addItem("Item7")
        self.listWidget.addItem("Item8")
        self.listWidget.addItem("Item9")
        self.listWidget.addItem("Item10")
        self.listWidget.addItem("Item11")

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


    def close_window(self):
        print('Escape Pressed')
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)

        # Set the central widget. Everything will be on top of this.
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)

        # Set the window properties
        self.setWindowTitle('Tracker')
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("QPushButton { font-size: 10pt;font-weight: bold}")

        # Read the last instance from trkr file
        pLastInstance = "saurabh.trkr"
        self.currentInstanceName = "Saurabh"
        self.currentInstance = DataFile(pLastInstance)

        # Child widgets on top of Central Widget
        self.calendar = " "
        self.slider = " "
        self.doubleSpinBox = " "

        # Layouts for the central widget
        self.main_layout = " "
        self.left_layout = " "
        self.right_layout = " "
        self.left_upper_layout = " "
        self.left_lower_layout = " "
        self.right_upper_layout = " "
        self.right_lower_layout = " "

        # Buttons on the central widget
        self.add_button = " "
        self.open_button = " "
        self.import_button = " "
        self.showlog_button = " "
        self.plot_button = " "
        self.save_button = " "

        # Variables used in the program
        self.lastModifiedDate = "Feb - 2 - 2020"
        self.lastValue = "110"
        self.currentSliderValue = 70
        self.currentDate = " "
        print(self.currentDate)
        self.size_policy_right_upper = " "
        self.size_policy_right_lower = " "

        # Create the layouts and the widgets contained in it
        self.create_layout()

    def create_layout(self):
        # _______________________________________________________________
        # |                             |                               |
        # |                             | Instance : Saurabh            |
        # |                             | Last Modified on: Feb-2-2020  |
        # |                             | Last Value : 110              |
        # |                             |                               |
        # |                             |_______________________________|
        # |       Calendar              |                               |
        # |                             |   Add +                       |
        # |                             |   Import                      |
        # |                             |   Show Log                    |
        # |                             |   Plot                        |
        # |_____________________________|   Save                        |
        # | Slider      |  DoubleSpin   |                               |
        # |             |     Box       |   Settings       Icon         |
        # |_____________|_______________|_______________________________|

        # MainLayout : The entire layout
        self.main_layout = QHBoxLayout(self.cw)

        # LeftLayout : Layout containing Calendar, Slider and LineEdit
        self.left_layout = QVBoxLayout(self.cw)

        # LeftUpperLayout(Part of LeftLayout): Layout containing Calendar
        self.left_upper_layout = QGridLayout(self.cw)
        self.left_upper_layout.addWidget(self.get_calendar_widget())

        # LeftLowerLayout(Part of LeftLayout) : Layout containing Slider and LineEdit
        self.left_lower_layout = QHBoxLayout(self.cw)
        self.left_lower_layout.addWidget(self.get_slider())
        self.left_lower_layout.addWidget(self.get_double_spin_box())

        # Adding the LeftUpper and LeftLower Layouts to the LeftLayout
        self.left_layout.addLayout(self.left_upper_layout)
        self.left_layout.addLayout(self.left_lower_layout)

        # RightLayout : Layout containing Instance information adn different buttons.
        self.right_layout = QVBoxLayout(self.cw)

        # RightUpperLayout : Layout containing Instance Information
        self.right_upper_layout = QVBoxLayout(self.cw)
        self.right_upper_layout.addStretch(1)
        self.right_upper_layout.setAlignment(Qt.AlignTop)
        self.right_upper_layout.addWidget(QLabel(
            "Instance : " + self.currentInstanceName + "\nLast modified on : " + self.lastModifiedDate + "\nLast "
                                                                                                         "value : " +
            self.lastValue))

        selectedDate = QLabel("\n\nSelcted Date : 2 Feb 2020")
        selectedDate.setFont(QFont("Times", 12, QFont.Black))

        valueOnSelectedDate = QLabel("Value on the date: 110")
        valueOnSelectedDate.setFont(QFont("Times", 12, QFont.Black))

        self.right_upper_layout.addWidget(selectedDate)
        self.right_upper_layout.addWidget(valueOnSelectedDate)

        # RightLowerLayout : Layout containing buttons and settings
        self.right_lower_layout = QVBoxLayout(self.cw)
        self.right_lower_layout.addStretch(3)
        self.right_lower_layout.setAlignment(Qt.AlignTop)
        self.create_buttons()
        self.right_lower_layout.addWidget(self.add_button)
        self.right_lower_layout.addWidget(self.open_button)
        self.right_lower_layout.addWidget(self.import_button)
        self.right_lower_layout.addWidget(self.showlog_button)
        self.right_lower_layout.addWidget(self.plot_button)
        self.right_lower_layout.addWidget(self.save_button)

        # Adding the RightUpper and RightLower layouts to the RightLayout
        self.right_layout.addLayout(self.right_upper_layout, 1)
        self.right_layout.addLayout(self.right_lower_layout, 5)

        # Adding the Left and Right Layouts to the main layout
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        # MainLayout is what we are using
        self.cw.setLayout(self.main_layout)

    def get_calendar_widget(self):
        current_year, current_month, current_date = map(int, list(str(datetime.now().date()).split('-')))

        self.calendar = QCalendarWidget(self.cw)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate(current_year, current_month, current_date))
        self.calendar.clicked.connect(self.set_current_date)
        self.set_current_date()
        return self.calendar

    def get_slider(self):
        self.slider = QSlider(Qt.Horizontal, self.cw)
        self.slider.setMinimum(0)
        self.slider.setMaximum(600)
        self.slider.setValue(70)
        self.slider.setTickPosition(2)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(5)

        self.slider.valueChanged.connect(lambda x: self.set_current_slider_value(x))
        return self.slider

    def get_double_spin_box(self):
        self.doubleSpinBox = QDoubleSpinBox(self.cw)
        self.doubleSpinBox.setValue(self.currentSliderValue)
        self.doubleSpinBox.setMaximum(120.0)
        return self.doubleSpinBox

    def create_buttons(self):
        self.add_button = QPushButton("Add +", self.cw)
        self.add_button.setFixedSize(300, 60)
        self.add_button.clicked.connect(self.add_instance)
        self.add_button.setShortcut(QKeySequence(Qt.Key_A))

        self.open_button = QPushButton("Open", self.cw)
        self.open_button.setFixedSize(300, 60)
        self.open_button.clicked.connect(self.open_instance)
        self.open_button.setShortcut(QKeySequence(Qt.Key_O))

        self.import_button = QPushButton("Import", self.cw)
        self.import_button.setFixedSize(300, 60)
        self.import_button.clicked.connect(self.import_data)
        self.import_button.setShortcut(QKeySequence(Qt.Key_I))

        self.showlog_button = QPushButton("Show Log", self.cw)
        self.showlog_button.setFixedSize(300, 60)
        self.showlog_button.clicked.connect(self.show_log)
        self.showlog_button.setShortcut(QKeySequence(Qt.Key_L))

        self.plot_button = QPushButton("Plot", self.cw)
        self.plot_button.setFixedSize(300, 60)
        self.plot_button.clicked.connect(self.plot_graph)
        self.plot_button.setShortcut(QKeySequence(Qt.Key_P))

        self.save_button = QPushButton("Save", self.cw)
        self.save_button.setFixedSize(300, 60)
        self.save_button.clicked.connect(self.save_file)
        self.save_button.setShortcut(QKeySequence(Qt.Key_S))

    def set_current_date(self):
        self.currentDate = int(self.calendar.selectedDate().toString("yyyy.MM.dd").replace('.', ''))
        print(self.currentDate)

    def set_current_slider_value(self, current_value):
        self.currentSliderValue = int(60 + (current_value / 10))
        self.doubleSpinBox.setValue(self.currentSliderValue)
        print("Current Slider Value : " + str(current_value) + "   Weight : " + str(self.currentSliderValue))

    def add_instance(self):
        print("Add Button Clicked")
        self.addWindow = AddInstanceWindow(self)
        self.addWindow.show()

    def open_instance(self):
        print("Opening instance")
        self.instanceSelectionWindow = InstanceSelectionWindow(self)
        self.instanceSelectionWindow.show()

    def import_data(self):
        print("Importing data")

    def show_log(self):
        print("Showing Log")

    def plot_graph(self):
        print("Plotting Graph")

    def save_file(self):
        print(self.currentDate)
        print(self.currentSliderValue)
        self.currentInstance.write_field(self.currentDate, self.currentSliderValue)


def get_dark_palette():
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    return dark_palette
