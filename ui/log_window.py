from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget, QShortcut, \
    QTableWidgetItem


class LogWindow(QMainWindow):
    def __init__(self, mainWindow, pRows, pColumns):
        QWidget.__init__(self)

        self.parentWindow = mainWindow
        self.numItems = pRows

        # if pRows > 20:
        self.rows = pRows
        # else:
        #    self.rows = 20  # Looks good :P

        self.columns = pColumns

        # Set the window properties
        self.set_window_properties()

        # Create the central widget
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        # Create the widgets
        self.create_widgets()

        # Create the layouts
        self.create_layout()

        # Fill the data in the QTableWidget
        self.fill_data()

        # So that user can close this window by pressing the Escape key
        self.escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.escape.activated.connect(self.close)

    def set_window_properties(self):
        self.setWindowTitle("Logs")
        self.setWindowIcon(QIcon('resources/logo.png'))
        self.setMinimumWidth(300)

    def create_layout(self):
        self.mainLayout = QVBoxLayout(self.cw)
        self.menuLayout = QHBoxLayout(self.cw)

        self.menuLayout.addWidget(QLabel("Menu"))

        self.dataLayout = QVBoxLayout(self.cw)
        self.dataLayout.addWidget(self.tableWidget)
        self.dataLayout.stretch(1)

        self.mainLayout.addLayout(self.menuLayout)
        self.mainLayout.addLayout(self.dataLayout)

    def create_widgets(self):
        self.tableWidget = QTableWidget(self.rows, self.columns)

        # So that there are no unwanted empty areas in the Log Window.
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        # Set the headers. Col1 Header = Date. Col2 Header = Instance Name
        self.tableWidget.setHorizontalHeaderLabels(["Date", self.parentWindow.currentInstanceName])
        self.tableWidget.setColumnWidth(0, 150)

        # Get the required size fot the table based on the volume of data
        tableSize = self.get_table_size()

        # Set the size of the QTableWidget and the Log Window accordingly.
        self.tableWidget.setMaximumSize(tableSize)
        self.setMaximumSize(tableSize)


    def get_table_size(self):
        # Find Row height
        tableHeight = self.tableWidget.horizontalHeader().height()
        tableWidth = self.tableWidget.verticalHeader().width() + 4

        for i in range(0, self.rows):
            tableHeight += self.tableWidget.rowHeight(i)

        for i in range(0, self.columns):
            tableWidth += self.tableWidget.columnWidth(i)

        tableSize = QSize(tableWidth, tableHeight)

        return tableSize

    def fill_data(self):
        date = 0
        value = 1
        for currentRow in range(0, self.numItems):
            for currentColumn in range(0, self.columns):
                temp = QTableWidgetItem()
                temp.setFlags(temp.flags() & ~Qt.ItemIsEditable)
                if currentColumn == 0:
                    # Current column is the date column
                    temp.setText(self.parentWindow.convert_int_to_date(self.parentWindow.data[currentRow][date]))
                else:
                    # Current column is the value column
                    temp.setText(str(self.parentWindow.data[currentRow][value]) + " " + self.parentWindow.unitName)
                self.tableWidget.setItem(currentRow, currentColumn, temp)
