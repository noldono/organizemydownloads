import os
import zipfile

def getAllFilesInPath(path: str):
    list_of_files = []
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    for root, dirs, files in os.walk(downloads_folder):
        for file in files:
            # Join the current directory path with the file name to get the full file path
            file_path = os.path.join(root, file)
            list_of_files.append(file_path)

    return list_of_files

def archiveAll(list_of_files, archive_name = "ArchivedDownloadsFolder.zip") -> None:
    file_paths = getAllFilesInPath("test") # TODO: Fix the path stuff
    with zipfile.ZipFile(archive_name, "w") as archive:
        for path in file_paths:
            archive.write(path)

    print(f"Archive '{archive_name}' created successfully.")


