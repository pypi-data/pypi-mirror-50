import re
import os
import shutil


def setup_kaggle(KAGGLE=False):
    if KAGGLE:
        x = [f for f in os.listdir(os.curdir) if re.search('kaggle.*\.json', f)]
        assert len(x) == 1, 'Too much kaggle.json files'
        assert re.match('kaggle.*\.json', x[0]), 'Upload kaggle.json file'
        if not os.path.exists('/root/.kaggle'):
            os.makedirs('/root/.kaggle')
        shutil.move(x[0], '/root/.kaggle/kaggle.json')
        os.chmod('/root/.kaggle/kaggle.json', 0o600)


def download_kaggle_data(DOWNLOAD_DATA=False, COMPETITION=None, DATA_DIR=None):
    if DOWNLOAD_DATA:
        os.system('{} -p {}'.format(COMPETITION, str(DATA_DIR)))


def unarchive_data(UNARCHIVE_DATA=False, FILES_TO_UNZIP=None, DATA_DIR=None, USE_SUBFOLDERS=False):
    if UNARCHIVE_DATA and FILES_TO_UNZIP:
        for filename in FILES_TO_UNZIP:
            if USE_SUBFOLDERS:
                dir_name = filename.split('.zip')[0]
            else:
                dir_name = ''
            shutil.unpack_archive(str(DATA_DIR/filename), extract_dir=str(DATA_DIR/dir_name))



if __name__ == '__main__':
    download_kaggle_data()