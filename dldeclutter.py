import os
import collections
from pprint import pprint

# Estensioni da riconoscere
AUDIO_FILES = ['mp3', 'wav', 'raw', 'wma', 'aiff', 'mp2']
VIDEO_FILES = ['webm', 'mp4', 'mpg', 'mpeg', 'avi', 'mov', 'flv', 'mkv', 'h264']
IMAGE_FILES = ['png', 'jpeg', 'jpg', 'gif', 'svg', 'tiff', 'tif', 'psd', 'bmp']
DOCS_FILES  = ['pdf', 'docs', 'latex', 'csv', 'xls', 'doc', 'xlsx', 'odt', 'tex']
COMPR_FILES = ['zip', '7z', 'z', 'pkg','rar', 'tar']

# Path home
BASE_PATH = os.path.expanduser('~')
DEST_DIRS = ['Music', 'Movies', 'Pictures', 'Documents', 'Applications', 'Other', 'Random']

for d in DEST_DIRS:
    dir_path = os.path.join(BASE_PATH, d)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

DOWNLOAD_PATH = os.path.join(BASE_PATH, 'Downloads')
files_mapping = collections.defaultdict(list)
files_list = os.listdir(DOWNLOAD_PATH)

for filename in files_list:
    if filename[0] != '.' : 
        file_ext = filename.split('.')[-1]
        files_mapping[file_ext].append(filename)


for f_ext, f_list in files_mapping.items() :
    if f_ext in AUDIO_FILES :
        for file in f_list :
            os.rename(
                os.path.join(DOWNLOAD_PATH, file), 
                os.path.join(BASE_PATH, 'Music', file))

    elif f_ext in DOCS_FILES or f_ext in COMPR_FILES:
        for file in f_list :
            os.rename(
                os.path.join(DOWNLOAD_PATH, file), 
                os.path.join(BASE_PATH, 'Documents', file))
    
    elif f_ext in VIDEO_FILES :
        for file in f_list :
            os.rename(
                os.path.join(DOWNLOAD_PATH, file), 
                os.path.join(BASE_PATH, 'Movies', file))

    elif f_ext in IMAGE_FILES :
        for file in f_list :
            os.rename(
                os.path.join(DOWNLOAD_PATH, file), 
                os.path.join(BASE_PATH, 'Pictures', file))
    
    else:
        for file in f_list :
            os.rename(
                os.path.join(DOWNLOAD_PATH, file), 
                os.path.join(BASE_PATH, 'Other', file))