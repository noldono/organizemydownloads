import os
import send2trash
import datetime
from enum import Enum


class Action(Enum):
    DELETE = 0
    ARCHIVE = 1


class File:
    """
    Initializes a file object with the given path
    """

    def __init__(self, path):
        self.path: str = path
        self.name: str
        self.type: str
        self.name, self.type = os.path.splitext(os.path.basename(path))
        self.type = self.type.strip('.').lower()
        self.size: int = os.path.getsize(path)
        self.last_accessed: float = os.path.getatime(path)
        self.date_added: float = os.path.getctime(path)
        self.last_accessed_formatted: str = datetime.datetime.fromtimestamp(self.last_accessed).strftime(
            '%Y/%m/%d %H:%M'
        )
        self.date_added_formatted: str = datetime.datetime.fromtimestamp(self.date_added).strftime(
            '%Y/%m/%d %H:%M'
        )
        self.checked: bool = False

    """
    Returns a string representation of the file object
    """

    def __str__(self):
        return (
            f"File Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Size: {self.size} bytes\n"
            f"Type: {self.type}\n"
            f"Last Accessed: {self.last_accessed_formatted}"
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
            print(f"Removed {self.name}")
            return True
        except OSError:
            return False
