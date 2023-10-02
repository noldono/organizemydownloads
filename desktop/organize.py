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


def get_duplicates(files):
    # keep track of duplicate files and unique files
    duplicates = []
    unique_files = []

    for file in files:
        duplicate = False
        for unique_file in unique_files:
            # if file types differ, skip
            if file.type != unique_file.type:
                continue

            # if file sizes differ, skip
            if file.size != unique_file.size:
                continue

            # if file names do not follow the Windows duplicate file name convention, skip
            # example: 'file.txt' and 'file (1).txt.'
            if file.name not in unique_file.name and unique_file.name not in file.name:
                continue

            # if file types, sizes, and names match, add to duplicates
            duplicates.append(file)
            duplicate = True
            break

        # if file is not a duplicate, add to unique files
        if not duplicate:
            unique_files.append(file)

    # return the list of duplicate files
    return duplicates
