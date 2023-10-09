from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#from layout_colorwidget import Color

import sys

import os
import send2trash
import datetime
import numpy as np


class File:
    """
    Initializes a file object with the given path
    """

    def __init__(self, path, action=""):
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)
        _, self.type = os.path.splitext(self.name)
        self.type = self.type.strip('.')
        self.last_accessed = np.round(os.path.getatime(path))
        self.action = action

    """
    Returns a string representation of the file object
    """

    def __str__(self):
        return (
            f"File: {self.name}\n"
            f"Path: {self.path}\n"
            f"Size: {self.size} bytes\n"
            f"Type: {self.type}\n"
            f"Last Accessed: {str(datetime.datetime.fromtimestamp(np.round(self.last_accessed)))}"
        )

    """
    Recycles the file at the given path
    Returns true if successful, false otherwise
    """

    def recycle(self):
        try:
            send2trash.send2trash(self.path)
            return True
        except send2trash.TrashPermissionError or OSError:
            return False

    """
    Deletes the file at the given path
    Returns true if successful, false otherwise
    """

    def delete(self):
        try:
            os.remove(self.path)
            return True
        except OSError:
            return False

    """
    Gets the action for the file
    """

    def getaction(self):
        return self.action


class MainWindow(QMainWindow):
    def __init__(self, display_files, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        Box_layout = QHBoxLayout()

        # Get screen size
        screen = app.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height()

        pageLayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stackLayout = QStackedLayout()

        pageLayout.addLayout(button_layout)
        pageLayout.addLayout(self.stackLayout)

        def activate_tab_1():
            self.stackLayout.setCurrentIndex(0)

        # def activate_tab_2():
        #     self.stacklayout.setCurrentIndex(1)
        #
        # def activate_tab_3():
        #     self.stacklayout.setCurrentIndex(2)

        btn = QPushButton("red")
        btn.clicked.connect(activate_tab_1)
        button_layout.addWidget(btn)

        # btn = QPushButton("green")
        # btn.pressed.connect(self.activate_tab_2)
        # button_layout.addWidget(btn)
        # self.stacklayout.addWidget(Color("green"))
        #
        # btn = QPushButton("yellow")
        # btn.pressed.connect(self.activate_tab_3)
        # button_layout.addWidget(btn)
        # self.stacklayout.addWidget(Color("yellow"))

        # Set the window size to half of the screen resolution
        self.resize((width // 3) * 2, (height // 3)*2)

        self.setWindowTitle("OrganizeMyDownloads")

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Filename", "Size", "Date accessed"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.horizontalHeader().sortIndicatorChanged.connect(self.sort_table)

        self.display_files = display_files

        # sample_files = [
        #     {"name": "fileA.txt", "size": "12 KB"},
        #     {"name": "fileB.txt", "size": "34 KB"},
        #     {"name": "fileC.txt", "size": "23 KB"},
        # ]

        for file in display_files:
            row_position = self.table.rowCount()
            date_time = datetime.datetime.fromtimestamp(file.last_accessed).strftime('%Y/%m/%d %H:%M')
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(file.name))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(file.size)))
            self.table.setItem(row_position, 2, QTableWidgetItem(date_time))
            # self.table.setItem(row_position, 3, QTableWidgetItem(file["size"]))

        #Box_layout.addWidget(self.table, alignment=None)
        self.stackLayout.addWidget(self.table)

        #self.setCentralWidget(self.table)
        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)

    def sort_table(self, column, order):
        self.table.sortItems(column, order)


newFile1 = File("C:/Users/evanj/Desktop/Senior/Fall 23/4574 Large Software/OrganizeMyDownloads/test1.txt")
newFile2 = File("C:/Users/evanj/Desktop/Senior/Fall 23/4574 Large Software/OrganizeMyDownloads/test2.txt")
newFile3 = File("C:/Users/evanj/Desktop/Senior/Fall 23/4574 Large Software/OrganizeMyDownloads/test3.txt")

print(str(newFile1.last_accessed))

files = [newFile1, newFile2, newFile3]

app = QApplication(sys.argv)
window = MainWindow(files)
window.show()

app.exec_()
