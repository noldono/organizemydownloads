from datetime import date, timedelta

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QDesktopWidget, QMenuBar, QPushButton, QLineEdit, \
    QHBoxLayout, QLabel, QComboBox, QMessageBox, QTableWidgetItem, QFileDialog, QActionGroup, QMenu, QAction
from PyQt5.QtGui import QIcon

import functions
# import organize
from filetable import FileTable
from file import File

DATE_THRESHOLDS: dict[str, timedelta] = {
    "1 Month": timedelta(days=30),
    "3 Months": timedelta(days=30 * 3),
    "6 Months": timedelta(days=30 * 6),
    "1 Year": timedelta(days=365),
    "2 Years": timedelta(days=365 * 2),
    "5 Years": timedelta(days=365 * 5),
}

SIZE_THRESHOLDS: dict[str, int] = {
    "100 MB": 100 * 1024 ** 2,
    "500 MB": 500 * 1024 ** 2,
    "1 GB": 1024 ** 3
}


class MainWindow(QMainWindow):

    def __init__(self, path, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # initialize window
        self._init_window()

        # initialize layout
        self.central_layout = QVBoxLayout(self)

        self.selected_date_threshold: timedelta = DATE_THRESHOLDS["1 Year"]

        self.selected_size_threshold = SIZE_THRESHOLDS["500 MB"]

        # initialize menu bar
        self._init_menu_bar()

        self.files = functions.get_all_files_in_path("")  # Empty string as argument means target downloads folder.

        self.currentFiles = self.files

        self._init_copy_button()

        # initialize file table
        self.table = FileTable(self.files)

        self._init_search_bar()

        self._init_refresh_button()

        self._update_extensions()

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
        identify_menu.addAction("Identify All").triggered.connect(self._identify_all)
        identify_menu.addAction("Identify Duplicate Files").triggered.connect(self._identify_duplicates)
        identify_menu.addAction("Identify Installers").triggered.connect(self._identify_installers)
        identify_menu.addAction("Identify Old Files").triggered.connect(self._identify_old_files)

        date_threshold_menu = QMenu("File Date Threshold", self)

        date_threshold_group = QActionGroup(self)
        for threshold in DATE_THRESHOLDS.keys():
            threshold_action = QAction(threshold, self)
            threshold_action.setCheckable(True)
            if threshold == "1 Year":
                threshold_action.setChecked(True)
            threshold_action.triggered.connect(self._handle_date_threshold_change)
            date_threshold_group.addAction(threshold_action)
        date_threshold_menu.addActions(date_threshold_group.actions())
        identify_menu.addMenu(date_threshold_menu)

        identify_menu.addAction("Identify Large Files").triggered.connect(self._identify_large_files)

        size_threshold_menu = QMenu("File Size Threshold", self)
        size_threshold_group = QActionGroup(self)
        for threshold in SIZE_THRESHOLDS.keys():
            threshold_action = QAction(threshold, self)
            threshold_action.setCheckable(True)
            if threshold == "500 MB":
                threshold_action.setChecked(True)
            threshold_action.triggered.connect(self._handle_size_threshold_change)
            size_threshold_group.addAction(threshold_action)
        size_threshold_menu.addActions(size_threshold_group.actions())
        identify_menu.addMenu(size_threshold_menu)

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

        # add "Organize" menu with actions
        organize_menu = self.menu_bar.addMenu("Organize")
        organize_menu.addAction("Organize Into Folders Based on File Type").triggered.connect(self._organize)

        self.central_layout.addWidget(self.menu_bar)

    def _handle_date_threshold_change(self):
        self.selected_date_threshold = DATE_THRESHOLDS[self.sender().text()]

    def _handle_size_threshold_change(self):
        self.selected_size_threshold = SIZE_THRESHOLDS[self.sender().text()]

    def _organize(self):
        warning_str = '''
        Please read before proceeding!
        
        The following function will move all of the files inside your downloads folder into different subdirectories within the downloads folder. We HIGHLY recommend you backup your downloads folder prior to this procedure. You can do this by going to Backup > Backup Downloads Folder.
        
        Are you sure you wish to proceed?
        '''
        self.msg = QMessageBox()
        self.msg.setWindowTitle("WARNING")
        self.msg.setText(warning_str)
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = self.msg.exec_()

        if ret == QMessageBox.Yes:
            functions.organize_into_folders(list(self.files.values()))

    def _identify_all(self):
        self._identify_installers()
        self._identify_duplicates()
        self._identify_old_files()
        self._identify_large_files()

    def _identify_installers(self):
        installers = functions.identify_installers(list(self.files.values()))
        self.table.select_files(installers)

    def _identify_duplicates(self):
        duplicate_files = functions.get_duplicates(self.files.values())
        self.table.select_files(duplicate_files)

    def _identify_old_files(self):
        old_files = functions.identify_old_files(list(self.files.values()), self.selected_date_threshold)
        self.table.select_files(old_files)

    def _identify_large_files(self):
        large_files = functions.identify_large_files(list(self.files.values()), self.selected_size_threshold)
        self.table.select_files(large_files)

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

        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(QLabel("Show:"))

        # (drop-down menu)
        self.comboBox = QComboBox()

        # Connect the combo box signal to the search function
        self.comboBox.currentTextChanged.connect(self._extension_search)

        self.search_layout.addWidget(self.comboBox)
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)

        self.search_layout.addStretch(1)

        self.central_layout.addLayout(self.search_layout)

    def _refresh_table(self):
        self.files = functions.get_all_files_in_path("")
        self.table.update_table_contents(list(self.files.values()))

    def _init_refresh_button(self):
        self.refresh_button = QPushButton(QIcon.fromTheme("view-refresh"), "Refresh")
        self.refresh_button.clicked.connect(self._refresh_table)
        self.search_layout.addWidget(self.refresh_button)

    def _select_all(self):
        self.table.select_all()

    def _deselect_all(self):
        self.table.deselect_all()

    def _delete_selected(self):
        files_to_delete = self.table.get_selected_files()
        if self._show_warning_popup(files_to_delete, True):
            functions.delete_files(files_to_delete)

    def _recycle_selected(self):
        files_to_recycle = self.table.get_selected_files()
        if self._show_warning_popup(files_to_recycle, False):
            functions.recycle_files(files_to_recycle)

    def _show_warning_popup(self, file_list: list[File], delete: bool):
        warning_popup = QMessageBox()
        warning_popup.setWindowTitle("WARNING")
        warning_popup.setIcon(QMessageBox.Warning)
        if len(file_list) == 0:
            warning_popup.setText("No files selected.")
            warning_popup.exec_()
            return False

        keyword = "delete" if delete else "recycle"
        warning_text = f"Are you sure you want to {keyword} the selected files?"
        for file in file_list:
            warning_text += f"\n- {file.name}.{file.type}"

        warning_popup.setText(warning_text)
        warning_popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return warning_popup.exec_() == QMessageBox.Yes

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
            file_object.checked = (item.checkState() == Qt.Checked)

    def _update_extensions(self) -> None:
        extensions: list[str] = list()

        for file in self.files.values():
            if file.type not in extensions:
                extensions.append(file.type)

        self.comboBox.clear()
        self.comboBox.addItem("All")
        self.comboBox.addItems(extensions)

    def _extension_search(self, search_string: str):
        if search_string == 'All':
            self.table.update_table_contents(list(self.files.values()))
        else:
            files_to_display = functions.search_by_extension(self.files, search_string)
            self.table.update_table_contents(list(files_to_display.values()))

    def _filename_search(self):
        search_string = self.search_bar.text()
        if search_string:
            files_to_display = self._search_by_filename(self.table.get_displayed_files(), search_string)
            self.table.update_table_contents(files_to_display)
        else:
            self.table.update_table_contents(list(self.files.values()))

    def _search_by_filename(self, files: list[File], search_string: str) -> list[File]:
        matches: list[File] = list()
        for file in files:
            if search_string.lower() in file.name.lower():
                matches.append(file)

        return matches

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
