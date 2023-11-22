from PyQt5.QtWidgets import *
from gui import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("placeholder")
    window.show()

    sys.exit(app.exec_())
