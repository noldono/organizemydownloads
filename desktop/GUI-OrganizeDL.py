from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from file import File
import sys
import datetime


class MainWindow(QMainWindow):

    def __init__(self, display_files, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # initialize window
        self._init_window()

        # initialize layout
        self.central_layout = QVBoxLayout(self)

        # initialize menu bar
        self._init_menu_bar()

        # initialize table
        self._init_table(["Filename", "Size", "Date Accessed", "Selected"])

        # initialize display files
        self._init_display_files(display_files)

        # set central widget layout
        widget = QWidget(self)
        widget.setLayout(self.central_layout)
        self.setCentralWidget(widget)

    def _init_window(self):
        # set window title
        self.setWindowTitle("OrganizeMyDownloads")

        # get screen resolution
        resolution = QDesktopWidget().screenGeometry()

        # window size is 2/3 of screen resolution
        window_width = 2 * (resolution.width() // 3)
        window_height = 2 * (resolution.height() // 3)

        self.resize(window_width, window_height)

    def _init_menu_bar(self):
        # initialize menu bar
        self.menu_bar = QMenuBar(self)

        # TODO: connect menu actions to functions as demonstrated below with 'Select All' and 'Deselect All'

        # add "Identify" menu with actions
        identify_menu = self.menu_bar.addMenu("Identify")
        identify_menu.addAction("Identify Duplicate Files")
        identify_menu.addAction("Identify Installers")

        # add "Delete" menu with actions
        delete_menu = self.menu_bar.addMenu("Delete")
        delete_menu.addAction("Delete Currently Selected Files")

        # add "Backup" menu with actions
        backup_menu = self.menu_bar.addMenu("Backup")
        backup_menu.addAction("Backup Downloads Folder")
        backup_menu.addAction("Restore Backup")

        # add "Select" menu with actions
        select_menu = self.menu_bar.addMenu("Select")
        select_menu.addAction("Select All").triggered.connect(self._select_all)
        select_menu.addAction("Deselect All").triggered.connect(self._deselect_all)

        self.central_layout.addWidget(self.menu_bar)

    def _select_all(self):
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 3)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.Checked)

    def _deselect_all(self):
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 3)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.Unchecked)

    def _init_table(self, header_labels: list[str]):
        # initialize table with correct number of columns
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(header_labels))

        # set column names (header labels)
        self.table.setHorizontalHeaderLabels(header_labels)

        # make table span entire window width
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # make table sortable
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.horizontalHeader().sortIndicatorChanged.connect(self.table.sortItems)

        # add table to central layout
        self.central_layout.addWidget(self.table)

    def _init_display_files(self, display_files: list[File]):
        # each row contains file name, size, last accessed date, and a checkbox
        for file in display_files:
            row = self.table.rowCount()
            date_time = datetime.datetime.fromtimestamp(file.last_accessed).strftime('%Y/%m/%d %H:%M')
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(f"{file.name}.{file.type}"))
            self.table.setItem(row, 1, QTableWidgetItem(f"{file.size} bytes"))
            self.table.setItem(row, 2, QTableWidgetItem(date_time))
            self.table.setItem(row, 3, self._create_checkbox())

    def _create_checkbox(self):
        # create a checkbox to be used in the table
        # TODO: figure out how to center the checkbox in the table cell
        checkbox = QTableWidgetItem()
        checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        checkbox.setCheckState(Qt.Unchecked)
        checkbox.setTextAlignment(Qt.AlignCenter)
        return checkbox


newFile1 = File("C:\\Users\\Adam\\Downloads\\test\\a.txt")
newFile2 = File("C:\\Users\\Adam\\Downloads\\test\\b.txt")
newFile3 = File("C:\\Users\\Adam\\Downloads\\test\\c.txt")

print(str(newFile1.last_accessed))

files = [newFile1, newFile2, newFile3]

app = QApplication(sys.argv)
window = MainWindow(files)
window.show()

app.exec_()
