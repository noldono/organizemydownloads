import os
import functions
import organize
from file import Action
from file import File

if __name__ == "__main__":
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    list_of_files = functions.getAllFilesInPath(downloads_folder)
    new_list = functions.removeInstallers(list_of_files)
    for file in new_list:
        if file.action == Action.DELETE:
            print(file.name, file.size)