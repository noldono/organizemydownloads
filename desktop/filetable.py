"""
Description:
This file contains the code for the FileTable class, which is used to unify the QTableWidget
and the File class.

Authors: Adam Lahouar, Evan Donohoe, Nolan Donovan
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem

from file import File
from functions import format_file_size

HEADER_LABELS = ["Filename", "Location", "Size", "Date Last Accessed", "Date Added", "Selected"]


def _get_file_location(file: File) -> str:
    length_to_strip = len(file.name) + 1 + len(file.type)
    return file.path[:-length_to_strip]


class FileTable(QTableWidget):
    def __init__(self, files: dict, *args, **kwargs):
        super(FileTable, self).__init__(*args, **kwargs)

        self._all_files = files
        self._selected_files = {}
        self.displayed_files = {}

        self._initialize_table_properties()
        self.update_table_contents(list(files.values()))

    def _initialize_table_properties(self):
        # Set up header labels
        self.setColumnCount(len(HEADER_LABELS))
        self.setHorizontalHeaderLabels(HEADER_LABELS)

        # Set column widths
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for column in range(1, len(HEADER_LABELS)):
            self.horizontalHeader().setSectionResizeMode(column, QHeaderView.ResizeToContents)

        # Set up sorting
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().sortIndicatorChanged.connect(self.sortItems)
        self.itemChanged.connect(self._handle_user_selection)

        # Connect checkbox to file selection
        self.itemChanged.connect(self._handle_user_selection)

    def update_table_contents(self, files_to_display: list[File]):
        # Clear previous contents
        self.setRowCount(0)
        self.displayed_files.clear()

        # Display new files
        for row, file in enumerate(files_to_display):
            self.insertRow(row)

            row_items = self._get_widgets_from_file(file)
            for column, item in enumerate(row_items):
                self.setItem(row, column, item)

            self.displayed_files[file.path] = file

    def _get_widgets_from_file(self, file: File) -> list[QTableWidgetItem]:
        widgets: list[QTableWidgetItem] = list()

        name_widget = QTableWidgetItem(f"{file.name}.{file.type}")
        name_widget.setData(Qt.UserRole, file)  # Store the file object reference
        widgets.append(name_widget)

        location_widget = QTableWidgetItem(_get_file_location(file))
        widgets.append(location_widget)

        size_widget = SortUserRoleItem()
        size_widget.setData(Qt.DisplayRole, format_file_size(file.size))
        size_widget.setData(Qt.UserRole, file.size)  # Set the size in bytes as user data
        size_widget.setTextAlignment(Qt.AlignCenter)
        widgets.append(size_widget)

        last_accessed_widget = QTableWidgetItem(file.last_accessed_formatted)
        last_accessed_widget.setTextAlignment(Qt.AlignCenter)
        widgets.append(last_accessed_widget)

        date_added_widget = QTableWidgetItem(file.date_added_formatted)
        date_added_widget.setTextAlignment(Qt.AlignCenter)
        widgets.append(date_added_widget)

        # Make every widget read-only except for the checkbox
        for widget in widgets:
            widget.setFlags(widget.flags() & ~Qt.ItemIsEditable)

        checkbox_widget = self._create_checkbox()
        if file.path in self._selected_files.keys():
            checkbox_widget.setCheckState(Qt.Checked)
        checkbox_widget.setTextAlignment(Qt.AlignCenter)
        widgets.append(checkbox_widget)

        return widgets

    def get_displayed_files(self) -> list[File]:
        return list(self.displayed_files.values())

    def _create_checkbox(self) -> QTableWidgetItem:
        checkbox = QTableWidgetItem()
        checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        checkbox.setCheckState(Qt.Unchecked)

        return checkbox

    def _handle_user_selection(self, item):
        if item.column() != 5:
            return

        file = self.item(item.row(), 0).data(Qt.UserRole)
        if file and item.checkState() == Qt.Checked:
            self._selected_files[file.path] = file
        else:
            self._selected_files.pop(file.path, None)

    def select_files(self, files_to_select: list[File]) -> None:
        for file in files_to_select:
            self._selected_files[file.path] = file

        for row in range(self.rowCount()):
            file = self.item(row, 0).data(Qt.UserRole)
            if file in files_to_select:
                self.item(row, 5).setCheckState(Qt.Checked)
                self._selected_files[file.path] = file

    def get_selected_files(self) -> list[File]:
        return list(self._selected_files.values())

    def select_all(self):
        for row in range(self.rowCount()):
            self.item(row, 5).setCheckState(Qt.Checked)
            file = self.item(row, 0).data(Qt.UserRole)
            self._selected_files[file.path] = file

    def deselect_all(self):
        for row in range(self.rowCount()):
            self.item(row, 5).setCheckState(Qt.Unchecked)
            file = self.item(row, 0).data(Qt.UserRole)
            self._selected_files.pop(file.path, None)


class SortUserRoleItem(QTableWidgetItem):
    def __lt__(self, other: QTableWidgetItem) -> bool:
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)
