import os
import time
import collections

from datetime import datetime
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Estensioni da riconoscere
AUDIO_FILES = ['mp3', 'wav', 'raw', 'wma', 'aiff', 'mp2']
VIDEO_FILES = ['webm', 'mp4', 'mpg', 'mpeg', 'avi', 'mov', 'flv', 'mkv', 'h264']
IMAGE_FILES = ['png', 'jpeg', 'jpg', 'gif', 'svg', 'tiff', 'tif', 'psd', 'bmp']
DOCS_FILES  = ['pdf', 'docs', 'latex', 'csv', 'xls', 'doc', 'xlsx', 'odt', 'tex']
COMPR_FILES = ['zip', '7z', 'z', 'pkg','rar', 'tar']

DEST_DIRS = ['Music', 'Movies', 'Pictures', 'Documents', 'Applications', 'Other', 'Random'] 

def move_files() :

    TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

    for d in DEST_DIRS:
        dir_path = os.path.join(BASE_PATH, d)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

    files_mapping = collections.defaultdict(list)
    files_list = os.listdir(DOWNLOAD_PATH)

    for filename in files_list:
        if filename[0] != '.' : 
            file_ext = filename.split('.')[-1]
            files_mapping[file_ext].append(filename)
            


    for f_ext, f_list in files_mapping.items() :
        if f_ext in AUDIO_FILES :
            for file in f_list :
                name = file.split('.')[0]
                name = str(name) + "-" + TIMESTAMP + "." + f_ext

                os.rename(
                    os.path.join(DOWNLOAD_PATH, file), 
                    os.path.join(BASE_PATH, 'Music', name))

        elif f_ext in DOCS_FILES or f_ext in COMPR_FILES:
            for file in f_list :
                name = file.split('.')[0]
                name = str(name) + "-" + TIMESTAMP + "." + f_ext
                os.rename(
                    os.path.join(DOWNLOAD_PATH, file), 
                    os.path.join(BASE_PATH, 'Documents',  name))
        
        elif f_ext in VIDEO_FILES :
            for file in f_list :
                name = file.split('.')[0]
                name = str(name) + "-" + TIMESTAMP + "." + f_ext

                os.rename(
                    os.path.join(DOWNLOAD_PATH, file), 
                    os.path.join(BASE_PATH, 'Movies', name))

        elif f_ext in IMAGE_FILES :
            for file in f_list :
                name = file.split('.')[0]
                name = str(name) + "-" + TIMESTAMP + "." + f_ext

                os.rename(
                    os.path.join(DOWNLOAD_PATH, file), 
                    os.path.join(BASE_PATH, 'Pictures', name))
        
        else:
            for file in f_list :
                name = file.split('.')[0]
                name = str(name) + "-" + TIMESTAMP + "." + f_ext
                os.rename(
                    os.path.join(DOWNLOAD_PATH, file), 
                    os.path.join(BASE_PATH, 'Other', name))

# Path home 
BASE_PATH = os.path.expanduser('~')

# Path cartella da osservare per i cambiamenti (nel nostro caso la cartella downlads)
DOWNLOAD_PATH = os.path.join(BASE_PATH, 'Downloads')

# Vogliamo controllare i cambiamenti sulla cartella osservata. 
class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        move_files()

# Istanza della classe che si occupa di controllare le modifiche.
event_handler = FileHandler()
observer = Observer()

observer.schedule(event_handler, DOWNLOAD_PATH, recursive=True)
observer.start()

try: 
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()


