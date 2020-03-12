from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QGridLayout, QCalendarWidget, QDoubleSpinBox, QSlider, QMessageBox

from ui.add_window import *
from ui.open_window import *
from ui.close_window import *
from ui.no_instance_window import *
from ui.graph_window import *

from database.datafile import *
from algorithms.quicksort import *

gFromCloseWindow = False
gFromOpenWindow = False
isChangeDone = False

UNIT_FIELD_ID = 1
UNIT_FROM_RANGE = 2
UNIT_TO_RANGE = 3


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)

        # First things first. Initialize the variables that we are going to use throughout the program.
        self.currentInstance = None
        self.currentInstanceName = "********"
        self.lastInstanceName = "********"
        self.lastModifiedDate = "********"
        self.lastValue = "********"
        self.currentValue = "********"
        self.currentSliderValue = "70"
        self.unitName = ""
        self.fromRange = 60  # Some Default Value
        self.toRange = 120  # Some Default Value

        # This list is used for displaying the date on the App.
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Contains the list of all the instances the user has created.
        # This list is used when the user tries to create a duplicate instance.
        # Also, it is used the OpenWindow for showing the list of instances.
        self.allInstances = []

        # Add items to allInstances
        self.add_instances_to_list()

        # Everything's done. Finally, set the current date form the system
        # so that we can use it for setting the current date of the calendar widget.
        self.set_current_date_from_system()

        self.set_window_properties()

        self.create_widgets()

        self.initialize_variables(None, None, None, None, False)

        self.create_layout()

    # ----------------------------------------------------------------#
    # Sets the main window properties : Title, Icon, Geometry and     #
    # Stylesheet                                                      #
    # ----------------------------------------------------------------#
    def set_window_properties(self):
        self.setWindowTitle('Tracker')
        self.setWindowIcon(QIcon('./resources/logo.png'))
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("QPushButton { font-size: 10pt;font-weight: bold}")

    # ----------------------------------------------------------------#
    # Creates all the widgets present in the Main Window. Doesn't add #
    # them to the screen.                                             #
    # ----------------------------------------------------------------#
    def create_widgets(self):

        # Set the central widget. Everything will be created on top of this
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)

        # Create the widgets used in the app
        self.calendar = self.get_calendar_widget()
        self.slider = self.get_slider(self.fromRange, self.toRange)
        self.doubleSpinBox = self.get_double_spin_box(self.toRange)

        # Create the buttons used in the app
        self.create_buttons()

        # A generic message box window to show different messages to the user
        self.msg = QMessageBox()
        self.msg.setWindowIcon(QIcon('resources/logo.png'))
        self.msg.setGeometry(300, 300, 600, 100)

    # ----------------------------------------------------------------#
    # Creates the button used in the app : Add, Open, Delete,         #
    # Show Log, Plot and Save                                         #
    # ----------------------------------------------------------------s#
    def create_buttons(self):
        self.add_button = QPushButton("Add +", self.cw)
        self.add_button.setFixedSize(300, 60)
        self.add_button.clicked.connect(self.add_instance)
        self.add_button.setShortcut(QKeySequence(Qt.Key_A))

        self.open_button = QPushButton("Open", self.cw)
        self.open_button.setFixedSize(300, 60)
        self.open_button.clicked.connect(self.open_instance)
        self.open_button.setShortcut(QKeySequence(Qt.Key_O))

        self.delete_button = QPushButton("Delete", self.cw)
        self.delete_button.setFixedSize(300, 60)
        self.delete_button.clicked.connect(self.delete_data)
        self.delete_button.setShortcut(QKeySequence(Qt.Key_I))

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

    # -------------------------------------------- #
    # Creates a QCalendarWidget and returns it     #
    # ---------------------------------------------#
    def get_calendar_widget(self):
        calendar = QCalendarWidget(self.cw)
        calendar.setGridVisible(True)
        calendar.setSelectedDate(QDate(int(self.current_year), int(self.current_month), int(self.current_date)))
        calendar.selectionChanged.connect(self.change_date_and_value)
        return calendar

    # -------------------------------------------- #
    # Creates a QSlider and returns it             #
    # ---------------------------------------------#
    def get_slider(self, pFromRange, pToRange):
        slider = QSlider(Qt.Horizontal, self.cw)
        slider.setMinimum(0)
        slider.setMaximum((pToRange - pFromRange) * 10)
        slider.setValue(pFromRange + ((pToRange - pFromRange) // 2))
        slider.setTickPosition(2)
        slider.setSingleStep(1)
        slider.valueChanged.connect(lambda x: self.set_current_slider_value(x))
        return slider

    def change_slider_properties(self, pFromRange, pToRange):
        self.slider.setMinimum(0)
        self.slider.setMaximum((pToRange - pFromRange) * 10)
        # self.slider.blockSignals(True)
        # self.slider.setValue(pFromRange + ((pToRange - pFromRange) // 2))
        self.set_current_slider_value(((pToRange - pFromRange) * 10) // 2, False, True)
        # self.slider.blockSignals(False)

    # -------------------------------------------- #
    # Creates a QDoubleSpinBox and returns it      #
    # ---------------------------------------------#
    def get_double_spin_box(self, pToRange):
        doubleSpinBox = QDoubleSpinBox(self.cw)
        doubleSpinBox.setMaximum(pToRange)

        # When value changes in Double Spin Box, it triggers the change of
        # value in the slider. When value changes in the slider, it triggers
        # a change in the value of the Double Spin Box. As we don't want to
        # fall into an infinite loop, thus we need to block signals here.
        doubleSpinBox.setValue(int(self.currentSliderValue))

        # When value changes in QSpinBox, same should be reflected in QSlider.
        doubleSpinBox.valueChanged.connect(lambda x: self.set_double_spin_box_value(x))

        return doubleSpinBox

    def change_double_spin_box_properties(self, pToRange):
        self.doubleSpinBox.blockSignals(True)
        self.doubleSpinBox.setMaximum(pToRange)
        self.doubleSpinBox.blockSignals(False)

    # ----------------------------------------------------------------#
    # This is our core function for creating the UI. All the created  #
    # widgets are placed on proper positions in the app in this        #
    # function only.                                                  #
    # ----------------------------------------------------------------#
    def create_layout(self):
        # _______________________________________________________________
        # |                             |                               |
        # |                             | Instance : Saurabh            |
        # |                             | Last Modified on: 2 Feb 2020  |
        # |                             | Last Value : 110              |
        # |                             |                               |
        # |                             | Date : Feb - 5 Feb 2020       |
        # |                             | Value: 70                     |
        # |                             |_______________________________|
        # |       Calendar              |                               |
        # |                             |   Add +                       |
        # |                             |   Open                        |
        # |                             |   Delete                      |
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

        # LeftLayout : Layout containing Calendar, Slider and DoubleSpinBox
        self.left_layout = QVBoxLayout(self.cw)

        # LeftUpperLayout(Part of LeftLayout): Layout containing Calendar
        self.left_upper_layout = QGridLayout(self.cw)
        self.left_upper_layout.addWidget(self.calendar)

        # LeftLowerLayout(Part of LeftLayout) : Layout containing Slider and DoubleSpinBox
        self.left_lower_layout = QHBoxLayout(self.cw)
        self.left_lower_layout.addWidget(self.slider)
        self.left_lower_layout.addWidget(self.doubleSpinBox)

        # Adding the LeftUpper and LeftLower Layouts to the LeftLayout
        self.left_layout.addLayout(self.left_upper_layout)
        self.left_layout.addLayout(self.left_lower_layout)

        # RightLayout : Layout containing Instance information and different buttons.
        self.right_layout = QVBoxLayout(self.cw)

        # RightUpperLayout : Layout containing Instance Information
        self.right_upper_layout = QVBoxLayout(self.cw)
        self.right_upper_layout.addStretch(1)
        self.right_upper_layout.setAlignment(Qt.AlignTop)
        self.right_upper_layout.addWidget(self.right_upper_top_label)
        self.right_upper_layout.addWidget(self.right_upper_bottom_label)

        # RightLowerLayout : Layout containing buttons and settings
        self.right_lower_layout = QVBoxLayout(self.cw)
        self.right_lower_layout.addStretch(3)
        self.right_lower_layout.setAlignment(Qt.AlignTop)
        self.right_lower_layout.addWidget(self.add_button)
        self.right_lower_layout.addWidget(self.open_button)
        self.right_lower_layout.addWidget(self.delete_button)
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

    # ----------------------------------------------------------------#
    # Initializes the member variables. This method would be called    #
    # during startup and every time a new instance is created or an   #
    # already existing instance is opened.                            #
    # --------------------------------------------------------------- #

    def initialize_variables(self, pInstanceName, pUnitName, pFromRange, pToRange, pFromOpenWindow):

        # All the in-memory value will be kept here.
        # This is the sole container for all our Date - Value info.
        self.data = []

        self.unitNameField = []

        if pInstanceName is None:  # This is None only during the startup

            # Check if there are instances already present on the disk. This would mean that
            # we have to open the last instance the user was working upon.
            if len([name for name in os.listdir('./logs/') if os.path.isfile(os.path.join('./logs/', name))]) is not 0:

                # Alright. So there are existing instances on the disk. Or at least the trkr
                # file is there.Open the trkr file to know the last instance that the user was working upon.
                self._trkr = DataFile("./logs/trkr")

                # Get the name of the last instance from the trkr file.
                self.lastInstanceName = self._trkr.read_ini_file().decode('UTF-8')

                # As we write the Last Instance Name to the trkr file only when the user
                # saves some data, this will happen if and only if the user has never saved
                # any data. It's kind of starting fresh.
                if self.lastInstanceName == "":
                    # We have nothing to do here as we already have the trkr file.
                    # So just return.
                    return
                else:
                    # So now we have a Last Instance Name. Check if the instance is actually present
                    # on the disk.
                    if os.path.exists("./logs/" + str(self.lastInstanceName)):
                        # Alright, the instance we were looking for is on the disk.

                        # Since this is the instance we are going to open, set it as the Current Instance Name
                        self.currentInstanceName = self.lastInstanceName

                        # Open the instance
                        self.currentInstance = DataFile("./logs/" + str(self.currentInstanceName))

                        # Read the data from it and save it to our sole container self.data[]
                        self.read_instance_from_disk()

                        # The user has the ability to delete all the data.
                        # She could have chosen to delete the file altogether. This would have made our life easier.
                        # But, To ERR IS HUMAN !!
                        if len(self.data):
                            self.lastModifiedDate = str(self.data[len(self.data) - 1][0])
                            self.lastModifiedDate = self.convert_int_to_date(self.lastModifiedDate)
                            self.lastValue = str(self.data[len(self.data) - 1][1])

                        self.change_slider_properties(self.fromRange, self.toRange)
                        self.change_double_spin_box_properties(self.toRange)
                    else:
                        # Oops! The user is a cruel person. She has deleted the instance manually from the disk.
                        # Also, she is a bit partial towards the trkr file, so she has not deleted or modified it.
                        # Consequently, the instance is there in the trkr file, but it doesn't exist on the disk. :-(a
                        # So like a responsible developer, we should show a proper message to the user to let her
                        # know what sin she has done.
                        self.msg.setWindowTitle("Oops!")
                        self.msg.setText("Oops!! Someone has deleted " + self.lastInstanceName + " from the "
                                                                                                 "disk.\nThe only"
                                                                                                 " rescue is to "
                                                                                                 "start fresh...")
                        self.msg.show()

                        # Make sure the next time we don't have to encounter the
                        # same situation.
                        self._trkr.write_ini_file("")
            else:
                # So there are no instances and not even the trkr file. So this is
                # kind of the first time the user is opening the app. All we have to do
                # here is to create the trkr file and let the user explore the app!
                self._trkr = DataFile("./logs/trkr")

        else:  # Alright. So the user is creating a new instance

            # If the user turns out to be lazy and doesn't save any data for the newly created instance
            # the current instance will serve as the last instance she was working upon. So save this value as we
            # might need it.
            self.lastInstanceName = self.currentInstanceName
            self.currentInstanceName = pInstanceName
            self.currentInstance = DataFile("./logs/" + str(self.currentInstanceName))
            self.allInstances.append(self.currentInstanceName)
            self.allInstances.sort()

            # The user trying to open an already existing instance from the Open Window
            if pFromOpenWindow:
                self.read_instance_from_disk()
                # Again, the user might have deleted all the data.
                if len(self.data):
                    self.lastModifiedDate = self.data[len(self.data) - 1][0]
                    self.lastModifiedDate = self.convert_int_to_date(self.lastModifiedDate)
                    self.lastValue = str(self.data[len(self.data) - 1][1])
            else:
                self.unitName = pUnitName
                self.unitName = self.unitName
                self.unitFieldLen = len(self.unitName)
                self.fromRange = pFromRange
                self.toRange = pToRange

            # We write to the ini file only if the last instance name makes some sense.
            if self.lastInstanceName != "********":
                self._trkr.write_ini_file(self.lastInstanceName)

    # ----------------------------------------------------------------#
    # This function is called when the user clicks the add button.    #
    # Creates a new window to take the name of the instance the user  #
    # wants to create. If a name is given, it creates the instance    #
    # physically.                                                     #
    # ----------------------------------------------------------------#
    def add_instance(self):
        # Save the current instance name. This will be used to know if the user has actually created
        # a new instance from the AddInstanceWindow
        self.prevInstanceName = self.currentInstanceName
        self.addWindow = AddInstanceWindow(self)
        self.addWindow.show()

    # ----------------------------------------------------------------#
    # Actually creates a physical instance on the disk. An instance   #
    # is created only if it is not already present on the disk.       #
    # Otherwise, a window is shown to the user to take appropriate    #
    # action.                                                         #
    # ----------------------------------------------------------------#
    def create_new_instance(self, pInstanceName, pUnitName, pFromRange, pToRange, pFromOpenWindow=False):
        # Set the currentInstance name and create the new file
        if pFromOpenWindow is False:
            # This ensures that we do not end up creating a duplicate instance
            if pInstanceName not in self.allInstances:

                # Close the currently opened file
                if self.currentInstance is not None:
                    self.currentInstance.close_file()

                self.initialize_variables(pInstanceName, pUnitName, pFromRange, pToRange, pFromOpenWindow)
                self.set_label_names()
            else:
                # The instance that the user is trying to create is already present.
                # We need to show her a proper message.
                self.msg.setWindowTitle("Duplicate Instance")
                self.msg.setText("An instance with the name \" " + pInstanceName + "\" is already present on the disk. "
                                                                                   "Please select a different name.")
                self.msg.show()
        else:
            # Close the currently opened file
            if self.currentInstance is not None:
                self.currentInstance.close_file()
            self.initialize_variables(pInstanceName, pUnitName, pFromRange, pToRange, pFromOpenWindow)
            self.set_label_names()

    # ----------------------------------------------------------------#
    # Shows the Instance Selection window                             #
    # ----------------------------------------------------------------#
    def open_instance(self):
        print("Opening instance")
        self.instanceSelectionWindow = InstanceSelectionWindow(self)
        self.instanceSelectionWindow.show()

    def delete_data(self):
        print("Importing data")

    def show_log(self):
        print("Showing Log")

    def plot_graph(self):
        self.graphWindow = GraphWindow(self)
        self.graphWindow.show()

    # ----------------------------------------------------------------#
    # This function is called when the user clicks the save button.   #
    # Clicking on save button saves the data in-memory only. The data #
    # is actually written to the disk only when the application is    #
    # closed                                                          #
    # ----------------------------------------------------------------#
    def save_data(self):
        # So the user is trying to save without creating an instance.
        # This can happen only when the user hasn't opened any instance.
        if self.currentInstance is None:
            # Show a proper message to the user and return
            self.noInstanceWindow = NoInstanceWindow(self)
            self.noInstanceWindow.show()
            return

        # Alright, so the user has done at least one change.
        # A change implies clicking the Save Button or deleting some value.
        # We use isChangeDone variable to decide whether to show a confirmation window
        # or not when the user tried closing the app. If no change has been done, the
        # confirmation window is not shown.
        # TODO: Set the variable in delete_data function too.
        global isChangeDone
        isChangeDone = True

        # Write the current instance name to the ini file so that
        # the next time the app opens, it opens this instance only.
        if self.currentInstance is not None:
            self._trkr.write_ini_file(self.currentInstanceName)

        # Get the current date and set it to last modified date
        # Last Modified Date is an integer representing the date.
        # Last Modified Date and Last Modified Value are written to the disk
        # so that the next time the application opens this instance, we can show these on the window.
        self.lastModifiedDate = self.convert_date_to_int(self.currentDate)
        self.lastValue = self.currentSliderValue

        # Obviously, as the user has clicked save, so she wants to see the same value
        # on the window.
        self.currentValue = self.currentSliderValue

        # Write everything in memory
        print(self.data)

        self.write_to_inmemory_list(self.lastModifiedDate, self.currentSliderValue)

        print(self.data)

        # We have written the date to the in-memory data. Now, change
        # it to a format in which it can be shown on the Main Window for the
        # last modified date label
        self.lastModifiedDate = self.currentDate

        # We have the updated values. Show it on the main window.
        self.set_label_names()

    # ----------------------------------------------------------------#
    # Writes the date - value pair to the sole in memory-container    #
    # ----------------------------------------------------------------#
    def write_to_inmemory_list(self, pDate, pValue):
        for i in self.data:
            # The user is modifying an already existing entry.
            if i[0] == pDate:
                i[1] = pValue
                return

        # The user is doing an entry for this date for the first time.
        self.data.append([pDate, pValue])

    def add_instances_to_list(self):
        instanceList = os.listdir('./logs/')
        instanceList.sort()
        for name in instanceList:
            if os.path.isfile(os.path.join('./logs/', name)) and name != "trkr":
                self.allInstances.append(name)

    def set_current_date_from_system(self):
        self.current_year, self.current_month, self.current_date = list(str(datetime.now().date()).split('-'))

        self.currentDate = str(self.current_date) + " " + str(self.months[int(self.current_month) - 1]) + " " + str(
            self.current_year)

    def closeEvent(self, event):
        # Opens the close window. Event is passed so that closing the app can be done from the close window.
        if gFromCloseWindow is False:
            if self.currentInstanceName != "********" and isChangeDone is True:
                self.closeWindow = CloseWindow(self)
                self.closeWindow.show()
                event.ignore()
        else:
            super(MainWindow, self).closeEvent(event)

    def read_instance_from_disk(self):
        self.data = self.currentInstance.read_file()
        print(self.data)
        self.data = self.create_in_memory_data()

    def create_in_memory_data(self):
        l = []
        for i in range(0, len(self.data), 2):
            if self.data[i] != UNIT_FROM_RANGE:
                l.append([self.data[i], self.data[i + 1]])
            else:
                self.read_meta_data(i)
                break
        return l

    def read_meta_data(self, pIndex):
        if self.data[pIndex] == UNIT_FROM_RANGE:
            self.fromRange = self.data[pIndex + 1]
            pIndex = pIndex + 2
        if self.data[pIndex] == UNIT_TO_RANGE:
            self.toRange = self.data[pIndex + 1]
            pIndex = pIndex + 2

        for i in range(pIndex + 1, len(self.data)):
            self.unitName = self.unitName + (chr(int(self.data[i])))

        print("From Range : " + str(self.fromRange))
        print("To Range : " + str(self.toRange))
        print("Unit Name :" + str(self.unitName))

    def set_label_names(self):
        self.right_upper_top_label.setText(
            "Instance Name : " + str(self.currentInstanceName) + "\nLast modified on : " + str(
                self.lastModifiedDate) + "\nLast Value : " + str(self.lastValue))
        self.right_upper_bottom_label.setText(
            "\n\nDate  : " + str(self.currentDate) + "\nValue : " + str(self.currentValue))

    def create_labels(self):
        self.right_upper_top_label = QLabel(self.cw)
        self.right_upper_bottom_label = QLabel(self.cw)
        self.right_upper_bottom_label.setFont(QFont("Times", 12, QFont.Black))
        self.set_label_names()

    def change_date_and_value(self):
        self.set_current_date()
        self.set_current_value(self.convert_date_to_int(self.currentDate))
        self.set_label_names()

    def set_current_date(self):
        self.current_date, self.current_month, self.current_year = self.calendar.selectedDate().toString(
            'dd-MM-yyyy').split('-')

        self.currentDate = str(self.current_date) + " " + str(self.months[int(self.current_month) - 1]) + " " + str(
            self.current_year)

    def set_current_value(self, pDate):
        for i in self.data:
            if int(i[0]) == int(pDate):
                self.currentValue = i[1]
                return

        self.currentValue = "********"

    def convert_date_to_int(self, pDate):
        if len(self.current_date) < 2:
            self.current_date = "0" + self.current_date

        return int(self.current_year + self.current_month + self.current_date)

    def set_current_slider_value(self, pCurrentValue, fromDoubleSpinBox=False, fromMetaData=False):
        self.currentSliderValue = int(self.fromRange + (pCurrentValue / 10))

        # Block signals so that vlaueChanged signal is not triggered for QDoubleSpinBox.
        # Else there will be a cyclic situation
        if not fromDoubleSpinBox:
            # When value changes in Slider, it triggers the change of
            # value in the Double Spin Box. When value changes in the Double Spin Box,
            # it triggers a change in the value of the Slider. As we don't want to
            # fall into an infinite loop, we need to block signals here.
            self.doubleSpinBox.blockSignals(True)
            self.doubleSpinBox.setValue(self.currentSliderValue)
            self.doubleSpinBox.blockSignals(False)

        if fromDoubleSpinBox or fromMetaData:
            self.slider.blockSignals(True)
            self.slider.setValue(pCurrentValue)
            self.slider.blockSignals(False)

    def set_double_spin_box_value(self, pCurrentValue):
        pCurrentValue = (pCurrentValue - self.fromRange) * 10
        self.set_current_slider_value(pCurrentValue, True)

    def convert_int_to_date(self, pDate):
        pDate = int(pDate)
        currentDate = pDate % 100
        pDate = pDate // 100
        currentMonth = self.months[(pDate % 100) - 1]
        pDate = pDate // 100
        currentYear = pDate
        return str(currentDate) + " " + currentMonth + " " + str(currentYear)

    def save_file(self):
        global gFromCloseWindow

        quicksort(self.data, 0, len(self.data) - 1)
        lastModifiedDate, lastModifiedMonth, lastModifiedYear = self.lastModifiedDate.split(' ')
        lastModifiedMonth = str(self.months.index(lastModifiedMonth) + 1)

        if len(lastModifiedMonth) < 2:
            lastModifiedMonth = "0" + lastModifiedMonth

        self.lastModifiedDate = int(lastModifiedYear + lastModifiedMonth + lastModifiedDate)
        self.data.append([self.lastModifiedDate, self.lastValue])

        for i in self.unitName:
            self.unitNameField.append(ord(i))

        self.data.append([UNIT_FROM_RANGE, self.fromRange])
        self.data.append([UNIT_TO_RANGE, self.toRange])
        self.data.append([(UNIT_FIELD_ID + self.unitFieldLen), self.unitNameField])

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
