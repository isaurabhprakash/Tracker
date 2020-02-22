from ui.main_window import *
from PyQt5.QtWidgets import QApplication

global window

if __name__ == '__main__':
    # Needed for all Qt Apps.
    app = QApplication([])

    app.setStyle('Fusion')

    # This is to set the Dark Mode.
    app.setPalette(get_dark_palette())

    # The main window of tracker. All the windows will be created from this
    # window
    window = MainWindow()

    window.show()

    app.exec_()