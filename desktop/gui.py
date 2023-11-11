from datetime import date

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QDesktopWidget, QMenuBar, QPushButton, QLineEdit, \
    QHBoxLayout, QLabel, QComboBox, QMessageBox, QTableWidgetItem, QFileDialog

import functions
import organize
from filetable import FileTable


class MainWindow(QMainWindow):

    def __init__(self, path, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # initialize window
        self._init_window()

        # initialize layout
        self.central_layout = QVBoxLayout(self)

        # initialize menu bar
        self._init_menu_bar()

        self.files = functions.get_all_files_in_path("")  # Empty string as argument means target downloads folder.

        self.currentFiles = self.files

        self._init_search_bar()

        self._update_extensions()

        self._init_copy_button()

        # initialize file table
        self.table = FileTable(self.files)

        # add file table to layout
        self.central_layout.addWidget(self.table)

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

        # add "Identify" menu with actions
        identify_menu = self.menu_bar.addMenu("Identify")
        identify_menu.addAction("Identify Duplicate Files").triggered.connect(self._identify_duplicates)
        identify_menu.addAction("Identify Installers").triggered.connect(self._identify_installers)

        # add "Delete" menu with actions
        delete_menu = self.menu_bar.addMenu("Delete")
        delete_menu.addAction("Delete Currently Selected Files").triggered.connect(self._delete_selected)
        delete_menu.addAction("Recycle Currently Selected Files").triggered.connect(self._recycle_selected)

        # add "Backup" menu with actions
        backup_menu = self.menu_bar.addMenu("Backup")
        backup_menu.addAction("Backup Downloads Folder").triggered.connect(self._archive_all)
        backup_menu.addAction("Restore Backup")

        # add "Select" menu with actions
        select_menu = self.menu_bar.addMenu("Select")
        select_menu.addAction("Select All").triggered.connect(self._select_all)
        select_menu.addAction("Deselect All").triggered.connect(self._deselect_all)

        self.central_layout.addWidget(self.menu_bar)

    def _identify_installers(self):
        installers = functions.identify_installers(self.files.values())
        self.table.select_files(installers)

    def _identify_duplicates(self):
        duplicate_files = organize.get_duplicates(self.files.values())
        self.table.select_files(duplicate_files)

    def _init_copy_button(self):
        # Create search button
        self.copy_button = QPushButton("Copy selected files to folder", self)
        self.copy_button.clicked.connect(self._copy_to_folder)

        self.central_layout.addWidget(self.copy_button)

    def _init_search_bar(self):
        # initialize menu bar
        self.search_bar = QLineEdit(self)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self._filename_search)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Show:"))

        # (drop-down menu)
        self.comboBox = QComboBox()

        # Connect the combo box signal to the search function
        # self.comboBox.currentTextChanged.connect(self._extension_search)

        search_layout.addWidget(self.comboBox)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)

        search_layout.addStretch(1)

        self.central_layout.addLayout(search_layout)

    def _select_all(self):
        self.table.select_all()

    def _deselect_all(self):
        self.table.deselect_all()

    def _delete_selected(self):
        functions.delete_files(self.table.get_selected_files())

    def _recycle_selected(self):
        functions.recycle_files(self.table.get_selected_files())

    def _archive_all(self):
        self.popup = QMessageBox()
        self.popup.setWindowTitle("Archive Status")
        self.popup.setText("Archive Started")
        self.popup.show()

        self.thread = ArchiveThread(self.files.values())
        self.thread.finished.connect(self._archive_finished)
        self.thread.start()

    def _archive_finished(self):
        self.popup = QMessageBox()
        self.popup.setWindowTitle("Archive Status")
        self.popup.setText(f"Archive Finished! Saved as downloads_archive_{date.today()}.zip")
        self.popup.show()

    def _create_checkbox(self):
        # create a checkbox to be used in the table
        # TODO: figure out how to center the checkbox in the table cell
        checkbox = QTableWidgetItem()
        checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        checkbox.setCheckState(Qt.Unchecked)
        checkbox.setTextAlignment(Qt.AlignCenter)

        return checkbox

    def _item_changed(self, item):
        # Check if the changed item is in the checkbox column
        if item.column() == 5:
            file_item = self.table.item(item.row(), 0)
            file_object = file_item.data(Qt.UserRole)

            # Update the file object based on the checkbox state
            if item.checkState() == Qt.Checked:
                file_object.checked = True
            else:
                file_object.checked = False

    def _update_extensions(self):
        # return list of all extension

        ext = []

        for file in self.currentFiles.values():
            if file.type not in ext:
                ext.append(file.type)

        self.comboBox.clear()
        self.comboBox.addItem("All")
        self.comboBox.addItems(ext)

    def _extension_search(self, search_string):
        if search_string == "All":
            self._display_files(self.files)
            self.currentFiles = self.files
        else:
            self.currentFiles = functions.search_by_extension(self.currentFiles, search_string)
            self._display_files(self.currentFiles)

    def _filename_search(self, search_string):
        search_string = self.search_bar.text()
        if search_string == "":
            self._display_files(self.files)
            self.currentFiles = self.files
        else:
            self.currentFiles = functions.search_by_filename(self.currentFiles, search_string)
            self._display_files(self.currentFiles)

    # To decide: cut vs. copy
    def _copy_to_folder(self):
        # Prompt the user to select a directory
        dst_dir = QFileDialog.getExistingDirectory(None, "Select Destination Directory")
        selectedDict = functions.get_selected(self.currentFiles)
        functions.copy_files_to_directory(dst_dir, selectedDict)


class ArchiveThread(QThread):
    finished = pyqtSignal()

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def run(self):
        # Simulate a time-consuming operation
        functions.archive_all(self.arg)
        self.finished.emit()
