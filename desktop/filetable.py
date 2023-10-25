from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt
from file import File
from functions import format_file_size

HEADER_LABELS = ["Filename", "Absolute Path", "Size", "Date Accessed", "Selected"]


class FileTable(QTableWidget):
    def __init__(self, files: dict, *args, **kwargs):
        super(FileTable, self).__init__(*args, **kwargs)

        self._all_files = files
        self._selected_files = {}
        self.displayed_files = {}

        self._initialize_table_properties()
        self.update_table_contents(list(files.values()))

    def _initialize_table_properties(self):
        self.setColumnCount(len(HEADER_LABELS))
        self.setHorizontalHeaderLabels(HEADER_LABELS)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.setColumnWidth(0, 600)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().sortIndicatorChanged.connect(self.sortItems)
        self.itemChanged.connect(self._handle_user_selection)

    def update_table_contents(self, files_to_display: list[File]):
        self.setRowCount(0)
        for file in files_to_display:
            row = self.rowCount()
            self.insertRow(row)

            file_name_item = QTableWidgetItem(f"{file.name}.{file.type}")
            file_name_item.setData(Qt.UserRole, file)  # Store the file object reference

            size_item = SortUserRoleItem()
            size_item.setData(Qt.DisplayRole, format_file_size(file.size))
            size_item.setData(Qt.UserRole, file.size)  # Set the size in bytes as user data

            self.setItem(row, 0, file_name_item)
            self.setItem(row, 1, QTableWidgetItem(file.path))
            self.setItem(row, 2, size_item)
            self.setItem(row, 3, QTableWidgetItem(file.last_accessed_formatted))
            self.setItem(row, 4, self._create_checkbox())

    def get_displayed_files(self) -> list[File]:
        return list(self.displayed_files.values())

    def _create_checkbox(self):
        checkbox = QTableWidgetItem()
        checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        checkbox.setCheckState(Qt.Unchecked)
        checkbox.setTextAlignment(Qt.AlignCenter)

        return checkbox

    def _handle_user_selection(self, item):
        if item.column() != 4:
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
                self.item(row, 4).setCheckState(Qt.Checked)
                self._selected_files[file.path] = file

    def get_selected_files(self) -> list[File]:
        return list(self._selected_files.values())

    def select_all(self):
        for row in range(self.rowCount()):
            self.item(row, 4).setCheckState(Qt.Checked)

        self._selected_files = self._all_files

    def deselect_all(self):
        for row in range(self.rowCount()):
            self.item(row, 4).setCheckState(Qt.Unchecked)

        self._selected_files = {}

class SortUserRoleItem(QTableWidgetItem):
    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)
