from ui.ui import *
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    app.setPalette(get_dark_palette())

    windows = MainWindow()
    windows.show()

    app.exec_()
