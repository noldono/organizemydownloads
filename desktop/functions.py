import os
import zipfile
from file import File
from file import Action
from datetime import date

"""
    Gets all files in a particular path, returns a list of paths
"""


def get_all_files_in_path(path: str) -> dict:
    all_files = {}
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    path_to_traverse = downloads_folder if path == "" else path

    for root, dirs, files in os.walk(path_to_traverse):
        for file in files:
            # Join the current directory path with the file name to get the full file path
            file_path = os.path.join(root, file)
            all_files[file_path] = File(file_path)

    return all_files


"""
    Archives all files in a given path
"""


def archive_all(list_of_files, archive_name=f"downloads_archive_{date.today()}.zip") -> None:
    with zipfile.ZipFile(archive_name, "w") as archive:
        for file in list_of_files:
            archive.write(file.path)

    print(f"Archive '{archive_name}' created successfully.")


"""
    Marks all installers for deletion
    Any file names that are of type .exe and contain the words 'setup' and 'install' will be eligible for removal
    Will return an updated list of files with items marked for deletion
"""


def remove_installers(list_of_files) -> list:
    substrings = ['setup', 'install', 'windows', 'win']
    for file in list_of_files:
        contains_substring = any(substring in file.name.lower() for substring in substrings)
        if file.type == 'exe' and contains_substring:
            file.action = Action.DELETE

    return list_of_files


"""
    Removes any files from given list
"""


def delete_files(files: list[File]):
    for file in files:
        file.delete()


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
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
