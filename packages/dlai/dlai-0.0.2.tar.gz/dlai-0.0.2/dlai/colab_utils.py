import re
import os
import shutil


def setup_kaggle():
    if KAGGLE:
        x = !ls kaggle*.json
        assert re.match('kaggle.*\.json', x[0]), 'Upload kaggle.json file'
        if not os.path.exists('~/.kaggle'):
            os.makedirs('~/.kaggle')
        !mv kaggle*.json ~/.kaggle/kaggle.json
        !chmod 600 ~/.kaggle/kaggle.json


def download_kaggle_data():
    if DOWNLOAD_DATA:
        !{COMPETITION} -p {str(DATA_DIR)}


def unarchive_data(USE_SUBFOLDERS=False):
    if UNARCHIVE_DATA and FILES_TO_UNZIP:
        for filename in FILES_TO_UNZIP:
            if USE_SUBFOLDERS:
                dir_name = filename.split('.zip')[0]
            else:
                dir_name = ''
            shutil.unpack_archive(str(DATA_DIR/filename), extract_dir=str(DATA_DIR/dir_name))



if __name__ == '__main__':
    KAGGLE = False
    COMPETITION = None
    DOWNLOAD_DATA = False
    DATA_DIR = None
    UNARCHIVE_DATA = False
    FILES_TO_UNZIP = []