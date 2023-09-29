import os
import functions
import organize

if __name__ == "__main__":
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    list_of_files = functions.getAllFilesInPath(downloads_folder)
    new_list = organize.sortByAttribute(list_of_files, "size", True)
    print(new_list)