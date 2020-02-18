from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QGridLayout, QCalendarWidget, QDoubleSpinBox, QSlider

from ui.addWindow import *
from ui.openwindow import *
from ui.closewindow import *

from database.datafile import *

months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)

        # Set the window properties
        self.set_window_properties()

        # Initialize Variables
        self.initialize_variables()

        # Set the central widget. Everything will be on top of this.
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)

        self.create_new_instance()

        # Write last instance to trk file

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
        self.size_policy_right_upper = " "
        self.size_policy_right_lower = " "

        # Create the layouts and the widgets contained in it
        self.create_layout()

    def set_window_properties(self):
        self.setWindowTitle('Tracker')
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("QPushButton { font-size: 10pt;font-weight: bold}")

    def initialize_variables(self, pInstanceName=None):

        if pInstanceName is None:
            # Check if this is not the first instance being created. Executed during loading.
            if len([name for name in os.listdir('./logs') if os.path.isfile(name)]) is not 0:
                # TODO: There are existing logs. Open the trkr file to know the last instance the user was working on
                self._trkr = DataFile("trkr")
                self.currentInstanceName = "saurabh.trkr"  # TODO: Read this from trkr
                self.lastInstanceName = self.currentInstanceName
                self.currentInstance = DataFile(self.currentInstanceName)  # TODO: Open the already existing file

                self.lastModifiedDate = "2nd-Feb-2020"  # TODO: Read this from self.currentInstance
                self.lastValue = 110  # TODO: Read this from self.currentInstance
            else:
                # First time
                self.currentInstance = None
                self.currentInstanceName = "********"
                self.lastInstanceName = "********"
                self.lastModifiedDate = "********"
                self.lastValue = "********"
                self.currentSliderValue = "********"
        else:  # User is creating a new instance
            self.lastInstanceName = self.prevInstanceName
            self.currentInstanceName = pInstanceName
            self.currentInstance = DataFile(self.currentInstanceName)
            self.lastModifiedDate = "********"
            self.lastValue = "********"

        self.current_year, self.current_month, self.current_date = map(int, list(str(datetime.now().date()).split('-')))
        print(self.current_year)
        print(self.current_month)
        print(self.current_date)
        self.currentDate = str(self.current_date) + " " + str(months[self.current_month - 1]) + " " + str(
            self.current_year)
        self.currentSliderValue = 70  # TODO: If currenDate has a value, show that

    def create_new_instance(self, pInstanceName=None):
        # Close the currently opened file
        if self.currentInstance is not None:
            self.currentInstance.close_file()

        # Set the currentInstance name and create the new file
        if pInstanceName is not None:
            self.initialize_variables(pInstanceName)
            self.set_label_names()

    def set_label_names(self):
        self.label_top.setText("Instance Name : " + str(self.currentInstanceName) + "\nLast modified on : " + str(
            self.lastModifiedDate) + "\nLast Value : " + str(self.lastValue))
        self.label_down.setText("\n\nDate  : " + str(self.currentDate) + "\nValue : " + str(self.currentSliderValue))

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

        # First we create all the labels we are going to use
        self.create_labels()

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
        self.right_upper_layout.addWidget(self.label_top)
        self.right_upper_layout.addWidget(self.label_down)

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

    def create_labels(self):
        self.label_top = QLabel(self.cw)
        self.label_down = QLabel(self.cw)
        self.set_label_names()
        self.label_down.setFont(QFont("Times", 12, QFont.Black))

    def change_date(self):
        self.set_current_date()
        print(self.currentDate)
        self.set_label_names()

    def get_calendar_widget(self):

        self.calendar = QCalendarWidget(self.cw)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate(self.current_year, self.current_month, self.current_date))
        self.calendar.clicked.connect(self.set_current_date)
        self.set_current_date()
        self.calendar.selectionChanged.connect(self.change_date)
        return self.calendar

    def get_slider(self):
        self.slider = QSlider(Qt.Horizontal, self.cw)
        self.slider.setMinimum(0)
        self.slider.setMaximum(600)
        self.slider.setValue(70)
        self.slider.setTickPosition(2)
        self.slider.setSingleStep(1)
        #self.slider.setPageStep(5)

        self.slider.valueChanged.connect(lambda x: self.set_current_slider_value(x))

        return self.slider

    def set_current_slider_value(self, pCurrentValue, fromDoubleSpinBox=False):
        print("\n\n--Passed Value : " + str(pCurrentValue) + "\n\n")

        self.currentSliderValue = int(60 + (pCurrentValue / 10))

        # Block signals so that vlaueChanged signal is not trigerred for QDoubleSpingBox.
        # Else there will be a cyclic situaton
        if not fromDoubleSpinBox:
            self.doubleSpinBox.blockSignals(True)
            self.doubleSpinBox.setValue(self.currentSliderValue)
            self.doubleSpinBox.blockSignals(False)

        if fromDoubleSpinBox:
            self.slider.blockSignals(True)
            self.slider.setValue(pCurrentValue)
            self.slider.blockSignals(False)

        print("Current Slider Value : " + str(pCurrentValue) + "   Weight : " + str(self.currentSliderValue))

    def set_double_spin_box_value(self, pCurrentValue):
        pCurrentValue = (pCurrentValue - 60) * 10

        self.set_current_slider_value(pCurrentValue, True)

        print("Current Slider Value : " + str(pCurrentValue) + "   Weight : " + str(self.currentSliderValue))

    def get_double_spin_box(self):
        self.doubleSpinBox = QDoubleSpinBox(self.cw)
        self.doubleSpinBox.setMaximum(120.0)

        # We don't want to trigger valueChanged signal here.
        # When value changes in QSpinBox, same should be reflected in QSlider
        self.doubleSpinBox.blockSignals(True)
        self.doubleSpinBox.setValue(self.currentSliderValue)
        self.doubleSpinBox.blockSignals(False)

        self.doubleSpinBox.valueChanged.connect(lambda x: self.set_double_spin_box_value(x))

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
        self.current_date, self.current_month, self.current_year = self.calendar.selectedDate().toString(
            'dd-MM-yyyy').split('-')
        self.currentDate = str(self.current_date) + " " + str(months[int(self.current_month) - 1]) + " " + str(
            self.current_year)

    def add_instance(self):
        print("Add Button Clicked")

        # Save the current instance name. This will be used to know if the user has actually created
        # a new instance from the AddInstanceWindow
        self.prevInstanceName = self.currentInstanceName
        self.addWindow = AddInstanceWindow(self)
        self.addWindow.show()

        print(self.currentInstanceName)
        # User has actually created a new instance
        if self.currentInstanceName != self.prevInstanceName:
            self.create_new_instance(self.currentInstanceName)

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
        # This is what will be written to the disk. Needs to be an integer by design
        self.lastModifiedDate = int(self.calendar.selectedDate().toString("yyyyMMdd"))
        self.set_current_date()
        print(self.currentDate)

        self.lastValue = self.currentSliderValue

        self.currentInstance.write_field(self.lastModifiedDate, self.currentSliderValue)

        self.lastModifiedDate = self.currentDate

        self.set_label_names()

    def close_window(self):
        self.closeWindow = CloseWindow(self)
        self.closeWindow.show()


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
