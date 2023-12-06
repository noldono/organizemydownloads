import os
import shutil
import zipfile
from datetime import date, datetime, timedelta

from file import Action
from file import File

import operator

directory_dict = {
    "Images": ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "svg", "icns", "heic"],
    "Documents": ["doc", "docx", "pdf", "txt", "odt", "rtf", "pages"],
    "Audio": ["mp3", "wav", "wma", "aac", "flac", "ogg", "aiff", "m4a"],
    "Video": ["mp4", "avi", "mov", "wmv", "flv", "mpeg", "m4v"],
    "Spreadsheets": ["xlsx", "xlsm", "xls", "ods", "numbers", "csv"],
    "Presentations": ["pptx", "ppt", "ppsx", "odp", "key"],
    "Code": ["py", "java", "c", "cpp", "html", "css", "js", "swift", "asm", "tpp", "h", "s"],
    "Archives": ["zip", "rar", "7z", "tar", "gz"],
    "Executables": ["exe", "dmg", "pkg", "app", "msi", "jar"],
    "Fonts": ["ttf", "otf", "woff2", "ttc", "dfont"],
}

"""
    Gets all files in a particular path, returns a list of paths
"""


def get_all_files_in_path(path: str) -> dict[str, File]:
    all_files: dict[str, File] = dict()
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
        if depth > 1:
            continue

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


def identify_old_files(list_of_files: list[File], threshold: timedelta) -> list[File]:
    """
    Returns a list of files that have not been created or accessed within the given threshold
    """
    old_files: list[File] = list()

    current_datetime = datetime.now()

    for file in list_of_files:
        date_added_delta = current_datetime - datetime.fromtimestamp(file.date_added)
        last_accessed_delta = current_datetime - datetime.fromtimestamp(file.last_accessed)

        if date_added_delta > threshold and last_accessed_delta > threshold:
            old_files.append(file)

    return old_files


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
        if search.lower() in file.name.lower():
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


def identify_large_files(file_list: list[File], size_threshold: int) -> list[File]:
    large_files: list[File] = list()
    for file in file_list:
        if file.size > size_threshold:
            large_files.append(file)

    return large_files


def organize_into_folders(files: list[File]) -> None:
    for file in files:
        downloads_folder = os.path.dirname(file.path)
        organized = False

        # Make sure current file isn't nested in a directory in the Downloads folder.
        if downloads_folder.endswith("Downloads"):
            for category, types in directory_dict.items():
                if file.type.lower() in types:
                    if not os.path.exists(f"{downloads_folder}\\{category}"):
                        os.makedirs(f"{downloads_folder}\\{category}")
                    dst = downloads_folder + f'\\{category}\\{file.name}.{file.type}'
                    shutil.move(file.path, dst)
                    organized = True
                    break

            if not organized:
                if not os.path.exists(f"{downloads_folder}\\Other"):
                    os.makedirs(f"{downloads_folder}\\Other")
                dst = downloads_folder + f'\\Other\\{file.name}.{file.type}'
                shutil.move(file.path, dst)


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


def get_duplicates(files) -> list[File]:
    duplicates = []
    seen = {}

    for file in files:
        file_key = (file.type, file.size)
        if file_key not in seen:
            seen[file_key] = [file]
            continue

        for seen_file in seen[file_key]:
            if file.name in seen_file.name:
                duplicates.append(seen_file)
                break

            if seen_file.name in file.name:
                duplicates.append(file)
                break

        seen[file_key].append(file)

    return duplicates
