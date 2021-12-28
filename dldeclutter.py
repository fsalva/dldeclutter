import os
import time
import collections

from datetime import datetime
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Extentions to be looked up:
AUDIO_FILES = ['mp3', 'wav', 'raw', 'wma', 'aiff', 'mp2']
VIDEO_FILES = ['webm', 'mp4', 'mpg', 'mpeg', 'avi', 'mov', 'flv', 'mkv', 'h264']
IMAGE_FILES = ['png', 'jpeg', 'jpg', 'gif', 'svg', 'tiff', 'tif', 'psd', 'bmp']
DOCS_FILES  = ['pdf', 'docs', 'latex', 'csv', 'xls', 'doc', 'xlsx', 'odt', 'tex']
COMPR_FILES = ['zip', '7z', 'z', 'pkg','rar', 'tar']

# Directiories we want to create (if non-existant) 
DEST_DIRS = ['Music', 'Movies', 'Pictures', 'Documents', 'Applications', 'Other', 'Random'] 

# Rename file, attaching a timestamp. 
def rename_file(ext_type, file_name, destination_folder) :
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    name = file_name.split('.')[0]
    name = str(name) + "-" + TIMESTAMP + "." + ext_type

    # Rename on filesystem
    os.rename(os.path.join(DOWNLOAD_PATH, file_name), os.path.join(BASE_PATH, destination_folder, name)) 

def create_directories() : 
    for d in DEST_DIRS:
        dir_path = os.path.join(BASE_PATH, d)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)


def move_files() :

    files_mapping = collections.defaultdict(list) # Gets a dictionary
    
    files_list = os.listdir(DOWNLOAD_PATH) # Gets all files in downloads folder

    for filename in files_list: 
        if filename[0] != '.' : # Ignore '.' folders
            file_ext = filename.split('.')[-1]  # Get extentions to create keys for the dictionary
            files_mapping[file_ext].append(filename) # Populate the dictionary
            
    # For each extentions, renames the files and moves it into the correct directory.
    for f_ext, f_list in files_mapping.items() :
        if f_ext in AUDIO_FILES :
            for file in f_list :
                rename_file(f_ext, file, 'Music')

        elif f_ext in DOCS_FILES or f_ext in COMPR_FILES:
            for file in f_list :
                rename_file(f_ext, file, 'Documents')
        
        elif f_ext in VIDEO_FILES :
            for file in f_list :
                rename_file(f_ext, file, 'Videos')

        elif f_ext in IMAGE_FILES :
            for file in f_list :
                rename_file(f_ext, file, 'Pictures')
                
        else:
            for file in f_list :
                rename_file(f_ext, file, 'Other')

# Path to home
BASE_PATH = os.path.expanduser('~')

# Path to download folder. 
DOWNLOAD_PATH = os.path.join(BASE_PATH, 'Downloads')

class FileHandler(FileSystemEventHandler):
    # When change occurs
    def on_modified(self, event):
        time.sleep(2)   # Give it some time to transfer the file [TODO: Breakable]
        move_files()    # Move it

# File system handler.
event_handler = FileHandler()
# File system observer
observer = Observer()

# Create the directories, if needed.
create_directories()

# Looks up for changes in DOWNLOAD_PATH
observer.schedule(event_handler, DOWNLOAD_PATH, recursive=True)
observer.start()

try: 
    # Always sleep until killed:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()


