import os
import zipfile
from file import File
from file import Action
from datetime import date

##for copy to folder
import shutil
from PyQt5.QtWidgets import QFileDialog

##

"""
    Gets all files in a particular path, returns a list of paths
"""


def get_all_files_in_path(path: str) -> dict:
    all_files = {}
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    path_to_traverse = downloads_folder if path == "" else path

    # Get the depth of the downloads folder
    # Example: C:\\Users\\Administrator\\Downloads
    # After split: ['C', 'Users', 'Administrator', 'Downloads']
    # Length: 4
    downloads_folder_depth = len(downloads_folder.split(os.sep))

    for root, dirs, files in os.walk(path_to_traverse):
        # Subtract the depth of the downloads folder from the depth of the path to get the relative depth
        depth = len(root.split(os.sep)) - downloads_folder_depth

        # We only care about files that are at most 1 subfolder deep (from the Downloads folder)
        if depth <= 1:
            for file in files:
                # Join the current directory path with the file name to get the full file path
                file_path = os.path.join(root, file)
                all_files[file_path] = File(file_path)

    return all_files


"""
    Archives all files in a given path
"""


def archive_all(list_of_files: list[File], archive_name=f"downloads_archive_{date.today()}.zip") -> None:
    with zipfile.ZipFile(archive_name, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in list_of_files:
            archive.write(file.path, os.path.relpath(file.path, os.path.commonpath([f.path for f in list_of_files])))

    print(f"Archive '{archive_name}' created successfully.")


"""
    Marks all installers for deletion
    Any file names that are of type .exe and contain the words 'setup' and 'install' will be eligible for removal
    Will return an updated list of files with items marked for deletion
"""


def remove_installers(list_of_files: list[File]) -> list[File]:
    substrings = ['setup', 'install', 'windows', 'win']
    installer_types = ['exe', 'msi']
    for file in list_of_files:
        contains_substring = any(substring in file.name.lower() for substring in substrings)
        if file.type in installer_types and contains_substring:
            file.action = Action.DELETE

    return list_of_files


def identify_installers(list_of_files: list[File]) -> list[File]:
    substrings = ['setup', 'install', 'windows', 'win']
    installer_types = ['exe', 'msi']
    installers = []
    for file in list_of_files:
        contains_substring = any(substring in file.name.lower() for substring in substrings)
        if file.type in installer_types and contains_substring:
            installers.append(file)

    return installers


"""
    Removes any files from given list
"""


def delete_files(files: list[File]):
    for file in files:
        file.delete()


"""
    Recycles any files from given list
"""


def recycle_files(files: list[File]):
    for file in files:
        file.recycle()


"""
    Format a file size to a human-readable string.

    File size ranges:
    - Less than 1 KB: Displays in bytes.
    - Between 1 KB and 1 MB: Displays in KB.
    - Between 1 MB and 1 GB: Displays in MB.
    - 1 GB or greater: Displays in GB.

    :param size_in_bytes: File size in bytes.
    :return: Formatted size as a string.
"""


def format_file_size(size_in_bytes: float):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} bytes"

    if size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"

    if size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"

    return f"{size_in_bytes / (1024 ** 3):.2f} GB"


"""
search_by_extension:
Searches given dict of file objects by extension

:param files_dict: Dict of file paths to copy
:return checked_dict: 
"""


def search_by_extension(files_dict: dict[str, File], search: str) -> dict:
    search_result_dict = {}

    for key, file in files_dict.items():
        if file.type == search:
            # file.checked = True
            search_result_dict[key] = file

    return search_result_dict


"""
search_by_filename:
Searches given dict of file objects by file name

:param files_dict: Dict of file paths to copy
:return checked_dict: 
"""


def search_by_filename(files_dict: dict[str, File], search: str) -> dict:
    search_result_dict = {}

    for key, file in files_dict.items():
        if search in file.name:
            # file.checked = True
            search_result_dict[key] = file

    return search_result_dict


"""
get_selected:
Gets file objects with 'True' checked values and returns new dict of them

:param files_dict: Dict of file paths to copy
:return checked_dict: 
"""


def get_selected(files_dict: dict[str, File]) -> dict:
    checked_dict = {}

    for key, file in files_dict.items():
        if file.checked:
            checked_dict[key] = file

    return checked_dict


"""
Prompts the user to select a directory and copies the given files to that directory.

:param files: Dict of file paths to copy
:param destination_directory: 
"""


def copy_files_to_directory(destination_directory: str, files: dict):
    if not destination_directory:
        print("No directory selected. Exiting.")
        return

    for file_path, file in files.items():
        try:
            shutil.copy(file_path, destination_directory)
            print(f"Successfully copied {file_path} to {destination_directory}")
        except Exception as e:
            print(f"Error copying {file_path}. Error: {e}")