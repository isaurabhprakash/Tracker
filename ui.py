from PyQt5.QtCore import Qt, QDate
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QStyleFactory, QLineEdit, QCalendarWidget, \
    QSlider, QGroupBox, QDialog, QDoubleSpinBox
from PyQt5.QtGui import QPalette, QColor


class WeightTracker(QWidget):

    def __init__(self, parent=None):
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

        # Variables
        self.currentInstanceName = "Saurabh"
        self.lastModifiedDate = "Feb - 2 - 2020"
        self.lastValue = "110"
        self.currentSliderValue = 70

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
        # |                             |   Export                      |
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
        self.right_upper_layout.addWidget(QLabel("Instance : " + self.currentInstanceName + "\nLast modified on : " + self.lastModifiedDate + "\nLast value : " + self.lastValue))

        # RightLowerLayout : Layout containing buttons and settings
        self.right_lower_layout = QVBoxLayout()
        self.right_lower_layout.addWidget(QPushButton("Add +"))
        self.right_lower_layout.addWidget(QPushButton("Open"))
        self.right_lower_layout.addWidget(QPushButton("Import"))
        self.right_lower_layout.addWidget(QPushButton("Export"))
        self.right_lower_layout.addWidget(QPushButton("Plot"))
        self.right_lower_layout.addWidget(QPushButton("Save"))




        # Adding the RightUpper and RightLower layouts to the RightLayout
        self.right_layout.addLayout(self.right_upper_layout)
        self.right_layout.addLayout(self.right_lower_layout)

        # Adding the Left and Right Layouts to the main layout
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        # MainLayout is what we are using
        self.setLayout(self.main_layout)

    def get_calendar_widget(self):
        global currentDate, currentMonth, currentYear

        currentYear, currentMonth, currentDate = map(int, list(str(datetime.now().date()).split('-')))

        self.calendar = QCalendarWidget(self);
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate(currentYear, currentMonth, currentDate))
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

    def set_current_slider_value(self, current_value):
        self.currentSliderValue = 60 + (current_value / 10)
        self.doubleSpinBox.setValue(self.currentSliderValue)
        print("Current Slider Value : " + str(current_value) + "   Weight : " + str(self.currentSliderValue))


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

    return dark_palette;


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    app.setPalette(get_dark_palette())

    windows = WeightTracker()

    # This code will be removed once the app is completely developed.
    # windows.setStyleSheet("""
    #     QWidget {
    #         border: 2px solid red;
    #         border-radius: 2px;
    #         }
    #     """)

    windows.show()

    app.exec_()
