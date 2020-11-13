import os
import time
import datetime
from shutil import copyfile


class FileLocator:
    def __init__(self):
        while True:
            self.file_updator()

    def file_updator(self):

        # Gets the recent modified file based on last modification
        # For windows file directory use // to get backslash
        latest_edited_file = max([file for file in os.scandir('SOURCE FILE LOCATION')],
                                 key=lambda last_changes: last_changes.stat().st_mtime).name

        try:
            # Copies file to new location with new name and format
            copyfile(f'SOURCE FILE LOCATION{latest_edited_file}',
                     'DESTINATION FILE LOCATION AND FILENAME WITH FORMAT/TYPE')

            print(f'{latest_edited_file} File Transferred Successful at {datetime.datetime.now()}')

        except IsADirectoryError:
            print(f'{latest_edited_file} File Transferred Unsuccessful at {datetime.datetime.now()}')

        time.sleep(10)


if __name__ == '__main__':
    FileLocator()
