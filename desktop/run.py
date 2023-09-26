import file
import functions

if __name__ == "__main__":
    list_of_files = functions.getAllFilesInPath("balls")
    functions.archiveAll(list_of_files)