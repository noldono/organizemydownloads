# OrganizeMyDownloads

## Table of Contents
- [How to Run](#how-to-run)
- [How It Works](#how-it-works)
- [Features](#features)
  - [Identify](#identify)
    - [Identify Duplicate Files](#identify-duplicate-files)
    - [Identify Installers](#identify-installers)
  - [Delete](#delete)
    - [Delete Currently Selected Files](#delete-currently-selected-files)
    - [Recycle Currently Selected Files](#recycle-currently-selected-files)
  - [Backup](#backup)
    - [Backup Downloads Folder](#backup-downloads-folder)
    - [Restore Backup](#restore-backup)
  - [Select](#select)
    - [Select All](#select-all)
    - [Deselect All](#deselect-all)
  - [Organize](#organize)
    - [Organize Into Folders Based on File Type](#organize-into-folders-based-on-file-type)

## How to Run
1. Clone the repository
2. Run the below command to install dependencies

```bash
python3 -m pip install -r requirements.txt
```
3. Run the below command in the project directory

```bash
python3 run.py
```

4. Enjoy!

## How It Works
The program will retireve a copy of your downloads folder and show all of the files within it. See the picture below
![image](https://github.com/noldono/organizemydownloads/assets/45012583/114ea3a1-6dc8-4b8f-b914-9f16935bae98)

Users can sort by size, name, date last accessed, or date added. Using the select box, you can delete, recycle, and organize files. If you'd like to backup your files prior to performing any operation, the Backup Downloads Folder feature will create an archive in the current working directory.

## Features
### Identify
- #### Identify Duplicate Files
  This feature will identify any duplicate files in the downloads folder. Duplicates, usually specific to windows, are files with ```(1)``` at the end of their file name. This, along with the size of the file are checked to verify that the marked files are duplicates. This feature will select the files that are deemed to be duplicates
- #### Identify Installers
  This will identify installers that are still in your downloads folder. Sometimes installers can take up significant space, so it's important to remove them if you don't need them anymore. Typically, on Mac, installers are deleted upon installation, so this feature targets Windows installers mainly.
### Delete
- #### Delete Currently Selected Files
  Will delete the currently selected files. A window will pop up confirming the removal.
- #### Recycle Currently Selected Files
  Will recycle the currently selected files assuming there is space in the recycling bin/trash for the selected files.
### Backup
- #### Backup Downloads Folder
  Spins up a thread in the background that creates an archive of the current downloads folder. The archive will be placed in the current project directory where ```run.py``` is located.
- #### Restore Backup
  **Currently Not Implemented**. To restore a backup, just extract the contents of the archive into the downloads folder.
### Select
- #### Select All
  Selects all files
- #### Deselect All
  Deselects all files
### Organize
- #### Organize Into Folders Based on File Type
  Creates a set of folders to organize each of the files into. These folders will contain files of various types, this is based on the following dictionary
  ```py
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
  ```
