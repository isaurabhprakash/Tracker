from PyQt5.QtCore import Qt, QDate
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QStyleFactory, QLineEdit, QCalendarWidget, \
    QSlider, QGroupBox, QDialog, QDoubleSpinBox, QSizePolicy
from PyQt5.QtGui import QPalette, QColor

from database.datafile import *


class WeightTracker(QWidget):

    def __init__(self, parent=None):
        # Read the last instance from trkr file
        pLastInstance = "saurabh.trkr"

        self.currentInstance = DataFile(pLastInstance)

        # Widgets
        self.calendar = " "
        self.slider = " "
        self.doubleSpinBox = " "

        # Layouts
        self.main_layout = " "
        self.left_layout = " "
        self.right_layout = " "
        self.left_upper_layout = " "
        self.left_lower_layout = " "
        self.right_upper_layout = " "
        self.right_lower_layout = " "

        # Buttons
        self.add_button = " "
        self.open_button = " "
        self.import_button = " "
        self.showlog_button = " "
        self.plot_button = " "
        self.save_button = " "

        # Variables
        self.currentInstanceName = "Saurabh"

        self.lastModifiedDate = "Feb - 2 - 2020"
        self.lastValue = "110"
        self.currentSliderValue = 70
        self.currentDate = " "
        print(self.currentDate)
        self.size_policy_right_upper = " "
        self.size_policy_right_lower = " "

        super(WeightTracker, self).__init__(parent)

        # Set the geometry
        self.setGeometry(0, 0, 800, 600)

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
        self.main_layout = QHBoxLayout()

        # LeftLayout : Layout containing Calendar, Slider and LineEdit
        self.left_layout = QVBoxLayout()

        # LeftUpperLayout(Part of LeftLayout): Layout containing Calendar
        self.left_upper_layout = QGridLayout()
        self.left_upper_layout.addWidget(self.get_calendar_widget())

        # LeftLowerLayout(Part of LeftLayout) : Layout containing Slider and LineEdit
        self.left_lower_layout = QHBoxLayout()
        self.left_lower_layout.addWidget(self.get_slider())
        self.left_lower_layout.addWidget(self.get_double_spin_box())

        # Adding the LeftUpper and LeftLower Layouts to the LeftLayout
        self.left_layout.addLayout(self.left_upper_layout)
        self.left_layout.addLayout(self.left_lower_layout)

        # RightLayout : Layout containing Instance information adn different buttons.
        self.right_layout = QVBoxLayout()

        # RightUpperLayout : Layout containing Instance Information
        self.right_upper_layout = QVBoxLayout()
        self.right_upper_layout.addStretch(1)
        self.right_upper_layout.setAlignment(Qt.AlignTop)
        self.right_upper_layout.addWidget(QLabel(
            "Instance : " + self.currentInstanceName + "\nLast modified on : " + self.lastModifiedDate + "\nLast "
                                                                                                         "value : " +
            self.lastValue))

        # RightLowerLayout : Layout containing buttons and settings
        self.right_lower_layout = QVBoxLayout()
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
        self.setLayout(self.main_layout)

    def get_calendar_widget(self):
        current_year, current_month, current_date = map(int, list(str(datetime.now().date()).split('-')))

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate(current_year, current_month, current_date))
        self.calendar.clicked.connect(self.set_current_date)
        self.set_current_date()
        return self.calendar

    def get_slider(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(600)
        self.slider.setValue(70)
        self.slider.setTickPosition(2)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(5)

        self.slider.valueChanged.connect(lambda x: self.set_current_slider_value(x))
        return self.slider

    def get_double_spin_box(self):
        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setValue(self.currentSliderValue)
        self.doubleSpinBox.setMaximum(120.0)
        return self.doubleSpinBox

    def create_buttons(self):
        self.add_button = QPushButton("Add +")
        self.add_button.setFixedSize(300, 60)

        self.open_button = QPushButton("Open")
        self.open_button.setFixedSize(300, 60)

        self.import_button = QPushButton("Import")
        self.import_button.setFixedSize(300, 60)

        self.showlog_button = QPushButton("Show Log")
        self.showlog_button.setFixedSize(300, 60)

        self.plot_button = QPushButton("Plot")
        self.plot_button.setFixedSize(300, 60)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(300, 60)
        self.save_button.clicked.connect(self.save_file)

    def set_current_date(self):
        self.currentDate = int(self.calendar.selectedDate().toString("yyyy.MM.dd").replace('.', ''))
        print(self.currentDate)

    def set_current_slider_value(self, current_value):
        self.currentSliderValue = int(60 + (current_value / 10))
        self.doubleSpinBox.setValue(self.currentSliderValue)
        print("Current Slider Value : " + str(current_value) + "   Weight : " + str(self.currentSliderValue))

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
