import os
import re
import time
import shutil
import typing

import eyed3
import requests

COUNTER = 1
FIRST_TIME = 0
TYPE = 'download'


def progress_hook(data):

    global COUNTER, FIRST_TIME, TYPE

    if data['status'] == 'downloading':
        print('#' * COUNTER if TYPE == 'download' else '.' * COUNTER, end='\r')
        time.sleep(0.5)
        COUNTER += 1
    elif data['total_bytes'] == data['downloaded_bytes']:
        COUNTER = 1
        print('\nDownloaded. Now converting.' if FIRST_TIME == 0 else '\nConverted.')
        FIRST_TIME += 1
        TYPE = 'convert'


def get_thumbnail(url: str) -> bool:
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open('thumbnail.jpg', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            f.close()
            return True
    else:
        return False


def construct_query(song_name: str) -> str:
    return '+'.join([word for word in re.split(r'\s', song_name) if len(word)])


def get_new_file_name(old_listdir_set: typing.Set[str]) -> str:
    return [
        file_name for file_name in set(os.listdir('.')).symmetric_difference(old_listdir_set) if
        file_name != 'thumbnail.jpg'
    ][0]


def assign_thumbnail(thumbnail_filename: str, audio_filename: str):
    audiofile = eyed3.load(audio_filename)

    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.images.set(3, open(thumbnail_filename, 'rb').read(), 'image/jpeg')

    audiofile.tag.save()
