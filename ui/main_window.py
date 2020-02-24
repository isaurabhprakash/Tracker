from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QGridLayout, QCalendarWidget, QDoubleSpinBox, QSlider, QMessageBox

from ui.add_window import *
from ui.open_window import *
from ui.close_window import *
from ui.no_instance_window import *

from database.datafile import *
from algorithms.quicksort import *

months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

gFromCloseWindow = False

isChangeDone = False


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)

        # All the in-memory value will be kept here
        self.data = []

        # Set the window properties
        self.set_window_properties()

        # Initialize Variables
        self.initialize_variables()

        # Set the central widget. Everything will be on top of this.
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)

        # Create the layouts and the widgets contained in it
        self.create_layout()

    def closeEvent(self, event):
        # Opens the close window. Event is passed so that closing the app can be done from the close window.
        if gFromCloseWindow is False:
            if self.currentInstanceName != "********" and isChangeDone is True:
                self.closeWindow = CloseWindow(self)
                self.closeWindow.show()
                event.ignore()
        else:
            super(MainWindow, self).closeEvent(event)

    def set_window_properties(self):
        self.setWindowTitle('Tracker')
        self.setWindowIcon(QIcon('./resources/logo.png'))
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("QPushButton { font-size: 10pt;font-weight: bold}")

    def initialize_variables(self, pInstanceName=None):

        if pInstanceName is None:
            # Check if this is not the first instance being created. Executed during loading.
            if len([name for name in os.listdir('./logs/') if os.path.isfile(os.path.join('./logs/', name))]) is not 0:
                # There are existing logs. Open the trkr file to know the last instance the user was working on
                self._trkr = DataFile("./logs/trkr")
                self.lastInstanceName = self._trkr.read_ini_file().decode('UTF-8')
                self.currentInstanceName = self.lastInstanceName
                if os.path.exists("./logs/" + str(self.currentInstanceName)) and self.currentInstanceName != "":
                    self.currentInstance = DataFile("./logs/" + str(self.currentInstanceName))
                    self.read_instance_from_disk()
                    self.lastModifiedDate = self.data[len(self.data) - 1][0]
                    self.lastModifiedDate = self.convert_int_to_date(self.lastModifiedDate)
                    self.lastValue = self.data[len(self.data) - 1][1]
                else:
                    # Someone has deleted the file manually. Create a fresh copy
                    # Someone might have opened the software and closed it without doing anything.
                    # In this case the trkr file gets generated but contains nothing. So currentInstanceName
                    # would be ""
                    if self.currentInstanceName != "":
                        self.initialize_variables(self.currentInstanceName)
                    else:
                        self.currentInstance = None
                        self.currentInstanceName = "********"
                        self.lastInstanceName = "********"
                        self.lastModifiedDate = "********"
                        self.lastValue = "********"
                        self.currentSliderValue = "********"
            else:
                # First time
                self._trkr = DataFile("./logs/trkr")
                self.currentInstance = None
                self.currentInstanceName = "********"
                self.lastInstanceName = "********"
                self.lastModifiedDate = "********"
                self.lastValue = "********"
                self.currentSliderValue = "********"
                # First time ever. Create the ini file
        else:  # User is creating a new instance
            self.lastInstanceName = self.currentInstanceName
            self.currentInstanceName = pInstanceName
            self.currentInstance = DataFile("./logs/" + str(self.currentInstanceName))
            self.lastModifiedDate = "********"
            self.lastValue = "********"
            if self.lastInstanceName != "********":
                self._trkr.write_ini_file(self.lastInstanceName)

        self.current_year, self.current_month, self.current_date = map(int, list(str(datetime.now().date()).split('-')))
        self.currentDate = str(self.current_date) + " " + str(months[self.current_month - 1]) + " " + str(
            self.current_year)
        self.currentSliderValue = 70  # TODO: If currentDate has a value, show that

    def read_instance_from_disk(self):
        self.data = self.currentInstance.read_file()
        self.data = self.create_in_memory_data()

    def create_in_memory_data(self):
        l = []
        for i in range(0, len(self.data), 2):
            l.append([self.data[i], self.data[i + 1]])
        return l

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
        # self.slider.setPageStep(5)

        self.slider.valueChanged.connect(lambda x: self.set_current_slider_value(x))

        return self.slider

    def set_current_slider_value(self, pCurrentValue, fromDoubleSpinBox=False):
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

    def set_double_spin_box_value(self, pCurrentValue):
        pCurrentValue = (pCurrentValue - 60) * 10
        self.set_current_slider_value(pCurrentValue, True)

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
        self.save_button.clicked.connect(self.save_data)
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

    def save_data(self):
        if self.currentInstanceName == "********":
            self.noInstanceWindow = NoInstanceWindow(self)
            self.noInstanceWindow.show()
            return
        global isChangeDone
        isChangeDone = True
        # Write the current instance name to the ini file so that
        # the next time the software open, it opens this instance only.
        if self.currentInstanceName != "********":
            self._trkr.write_ini_file(self.currentInstanceName)

        # Get the current date and set it to last modified date
        # Last Modified Date is an integer representing the date
        # This is what will be written to the disk.
        self.lastModifiedDate = int(self.calendar.selectedDate().toString("yyyyMMdd"))

        # Current Date is what is shown on the software as a Label
        self.set_current_date()

        self.lastValue = self.currentSliderValue

        # Write everything in memory
        self.write_to_inmemory_list(self.lastModifiedDate, self.currentSliderValue)

        print(self.data)

        # We have written the date to the in-memory data. Now, change
        # it to a format in which it can be shown on the Main Window for the
        # last modified date label
        self.lastModifiedDate = self.currentDate

        # We have the updated values. Show it on the main window.
        self.set_label_names()

    def write_to_inmemory_list(self, pDate, pValue):
        for i in self.data:
            if i[0] == pDate:
                i[1] = pValue
                return

        self.data.append([pDate, pValue])

    def convert_int_to_date(self, pDate):
        currentDate = pDate % 100
        pDate = pDate // 100
        currentMonth = months[(pDate % 100) - 1]
        pDate = pDate //100
        currentYear = pDate
        return str(currentDate) + " " + currentMonth + " " + str(currentYear)

    def save_file(self):
        global gFromCloseWindow
        quicksort(self.data, 0, len(self.data) - 1)
        lastModifiedDate, lastModifiedMonth, lastModifiedYear = self.lastModifiedDate.split(' ')
        lastModifiedDate = lastModifiedDate
        lastModifiedYear = lastModifiedYear
        lastModifiedMonth = str(months.index(lastModifiedMonth) + 1)
        if lastModifiedMonth < 10:
            lastModifiedMonth = "0"+lastModifiedMonth
        self.lastModifiedDate = int(lastModifiedYear + lastModifiedMonth + lastModifiedDate)
        self.data.append([self.lastModifiedDate, self.lastValue])
        for i in self.data:
            self.currentInstance.write_field(i[0], i[1])

        gFromCloseWindow = True
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        event.accept()


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
