import shutil

from file import File
import os
import operator

directory_dict = {
    "Images": ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "svg", "icns", "heic"],
    "Documents": ["doc", "docx", "pdf", "txt", "odt", "rtf", "pages"],
    "Audio": ["mp3", "wav", "wma", "aac", "flac", "ogg", "aiff", "m4a"],
    "Video": ["mp4", "avi", "mov", "wmv", "flv", "mpeg", "m4v"],
    "Spreadsheets": ["xlsx", "xlsm", "xls", "ods", "numbers", "csv"],
    "Presentations": ["pptx", "ppt", "ppsx", "odp", "key"],
    "Code": ["py", "java", "c", "cpp", "html", "css", "js", "swift", "asm", "tpp", "h", "s"],
    "Archives": ["zip", "rar", "7z"],
    "Compressed Files": ["zip", "rar", "7z", "tar", "gz"],
    "Executables": ["exe", "dmg", "pkg", "app", "msi", "jar"],
    "Fonts": ["ttf", "otf", "woff2", "ttc", "dfont"],
}

def organize_into_folders(files):
    for file in files:
        downloads_folder = os.path.dirname(file.path)
        organized = False

        # Make sure current file isn't nested in a directory in the downloads folder.
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
