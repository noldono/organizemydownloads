from file import File
import os
import operator

directory_dict = {
    'Images': ['png', 'jpg', 'jpeg'],
    'Videos': ['mp4', 'mov', 'avi', 'mkv'],
    'Audio': ['mp3', 'wav', 'flac'],
    'Documents': ['doc', 'docx', 'txt', 'pdf'],
    'Installers': ['exe', 'msi'],
    'Archives': ['zip', 'rar', '7z'],
}


def organize(files):
    for file in files:
        organized = False
        for category, types in directory_dict.items():
            if file.type in types:
                os.renames(file.path, os.path.join(category, file.name))
                organized = True
                break

        if not organized:
            os.renames(file.path, os.path.join('Other', file.name))


"""
    Sort the list of files by one of their attributes
"""


def sortByAttribute(list_of_files, attribute, descending=False):
    attributes = ["name", "size", "type", "last_accessed"]

    if attribute in attributes:
        # Define a mapping of attribute names to corresponding operators
        attribute_mapping = {
            "name": operator.attrgetter("name"),
            "size": operator.attrgetter("size"),
            "type": operator.attrgetter("type"),
            "last_accessed": operator.attrgetter("last_accessed")
        }

        # Sort the list of files based on the selected attribute
        if descending:
            list_of_files = sorted(list_of_files, key=attribute_mapping[attribute], reverse=True)
        else:
            list_of_files = sorted(list_of_files, key=attribute_mapping[attribute])

        return list_of_files

    return list_of_files
