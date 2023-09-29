import os
import zipfile
from file import File
from datetime import date

"""
    Gets all files in a particular path, returns a list of paths
"""


def getAllFilesInPath(path: str):
    list_of_files = []
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    path_to_traverse = downloads_folder if path == "" else path

    for root, dirs, files in os.walk(path_to_traverse):
        for file in files:
            # Join the current directory path with the file name to get the full file path
            file_path = os.path.join(root, file)
            list_of_files.append(File(file_path))

    return list_of_files


"""
    Archives all files in a given path
"""


def archiveAll(list_of_files, archive_name=f"downloads_archive_{date.today()}.zip") -> None:
    with zipfile.ZipFile(archive_name, "w") as archive:
        for file in list_of_files:
            archive.write(file.path)

    print(f"Archive '{archive_name}' created successfully.")
