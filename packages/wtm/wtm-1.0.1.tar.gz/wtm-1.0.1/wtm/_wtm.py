import os
import typing

import youtube_dl
import prettytable

from . import lib
from . import utils
from . import loggers

BASE_YOUTUBE_URL = 'http://www.youtube.com'
BASE_YOUTUBE_SEARCH_URL = BASE_YOUTUBE_URL + '/results?search_query={}'

table = prettytable.PrettyTable()
table.field_names = ['id', 'title', 'video link']


def wtm(song_name: str = None, select_top_result: bool = False) -> typing.Tuple[str, bool]:

    titles = lib.get_titles(song_name)
    if titles[0][0] == -1:
        return "Error from YouTube's side.", False

    for title in titles:
        table.add_row(title[:-1])

    print(table)

    if select_top_result:
        option = 1
    else:
        try:
            option = input('\nEnter most relevant title id : ')
        except KeyboardInterrupt:
            return '\nInterrupted.', False

    try:
        option = int(option)
    except ValueError:
        return 'Please enter a valid id.', False

    if option <= 0 or option > len(titles):
        return 'Please enter a valid id.', False

    postprocessors: typing.List[typing.Dict[str, str]] = [
        {
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            'key': 'FFmpegExtractAudio',
        }
    ]

    dir_listing_before_downloading = os.listdir('.')

    with youtube_dl.YoutubeDL(
            {
                'postprocessors': postprocessors,
                'logger': loggers.LowVerbosityLogger(),
                'progress_hooks': [utils.progress_hook],
            }
    ) as ydl:
        utils.get_thumbnail(titles[option - 1][3])
        ydl.download([titles[option - 1][2]])

    new_file_name = utils.get_new_file_name(set(dir_listing_before_downloading))
    utils.assign_thumbnail('thumbnail.jpg', new_file_name)
    os.rename(new_file_name, titles[option - 1][1] + '.mp3')
    os.remove('thumbnail.jpg')

    return 'done.', True
