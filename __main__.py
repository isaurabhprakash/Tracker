from ui.mainwindow import *
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    app.setPalette(get_dark_palette())

    window = MainWindow()
    window.show()

    app.exec_()