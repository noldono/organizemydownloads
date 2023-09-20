from file import File
import os

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
