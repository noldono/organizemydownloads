from PyQt5.QtWidgets import *
from gui import MainWindow
import sys

"""
Description:
Running this file will open the GUI

Authors: Nolan Donovan
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("")
    window.show()

    sys.exit(app.exec_())
