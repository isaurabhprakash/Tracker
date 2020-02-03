from PyQt5.QtCore import Qt, QDate
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QStyleFactory, QLineEdit, QCalendarWidget, \
    QSlider, QGroupBox, QDialog

from PyQt5.QtGui import QPalette, QColor


class WeightTracker(QWidget):

    def __init__(self, parent=None):
        self.calendar = " "
        self.main_layout = " "
        self.left_layout = " "
        self.right_layout = " "
        self.left_upper_layout = " "
        self.left_lower_layout = " "

        super(WeightTracker, self).__init__(parent)

        # Set the geometry
        self.setGeometry(0, 0, 800, 600)

        # Create the layouts and the widgets contained in it
        self.create_layout()

    def create_layout(self):
        # _______________________________________________
        # |                             |               |
        # |                             |               |
        # |                             |               |
        # |                             |               |
        # |                             |               |
        # |       Calendar              |               |
        # |                             |               |
        # |                             | Right-Layout  |
        # |                             |               |
        # |                             |               |
        # |                             |               |
        # |                             |               |
        # |_____________________________|               |
        # |               |             |               |
        # | Slider        |  LineEdit   |               |
        # |               |             |               |
        # |_______________|_____________|_______________|

        # MainLayout : The entire layout
        self.main_layout = QHBoxLayout()

        # LeftLayout : Layout containing Calendar, Slider and LineEdit
        self.left_layout = QVBoxLayout()

        # LeftUpperLayout(Part of LeftLayout): Layout containing Calendar
        self.left_upper_layout = QGridLayout()
        self.left_upper_layout.addWidget(self.get_calendar_widget())

        # LeftLowerLayout(Part of LeftLayout) : Layout containing Slider and LineEdit
        self.left_lower_layout = QHBoxLayout()
        self.left_lower_layout.addWidget(QSlider(Qt.Horizontal))
        self.left_lower_layout.addWidget(QLabel("Just a label"))

        # Adding the LeftUpper and LeftLower Layouts to the LeftLayout
        self.left_layout.addLayout(self.left_upper_layout)
        self.left_layout.addLayout(self.left_lower_layout)

        # RightLayout : Containing 2 Labels for now
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(QLabel("Upper Text"))
        self.right_layout.addWidget(QLabel("Lower Text"))

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
