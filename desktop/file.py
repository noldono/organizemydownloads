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

    def __init__(self, path, action=""):
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)
        _, self.type = os.path.splitext(self.name)
        self.name = self.name.strip(self.type)
        self.type = self.type.strip('.')
        self.last_accessed = os.path.getatime(path)
        self.last_accessed_formatted = datetime.datetime.fromtimestamp(self.last_accessed).strftime('%Y/%m/%d %H:%M')
        self.action = action

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
            return True
        except OSError:
            return False

    """
    Gets the action for the file
    """

    def getaction(self):
        return self.action
