import re
import typing

import bs4
import requests

from . import _wtm
from . import utils


def get_titles(song_name: str, ) -> typing.List[typing.Tuple[int, str, str, str]]:

    # make request to YouTube search
    query = utils.construct_query(song_name)
    response: requests.Response = requests.get(_wtm.BASE_YOUTUBE_SEARCH_URL.format(query))

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        titles = []
        # Kind of a complex data structure -
        #     [(#1, Title #1, link for #1, thumbnail url for #1),
        #      (#2, Title #2, link for #2, thumbnail url for #1),
        #      (#3, Title #3, link for #3, thumbnail url for #1),]
        for index, title in enumerate(soup.findAll(attrs={'class': 'yt-uix-tile-link'})):
            link = _wtm.BASE_YOUTUBE_URL + title['href']
            thumbnail_url = 'http://img.youtube.com/vi/{}/0.jpg'.format(
                re.findall(r'^.*((youtu.be/)|(v/)|(/u/\w/)|(embed/)|(watch\?))\??v?=?([^#&?]*).*', link)[-1][-1]
            )
            titles.append((index+1, title.text, link, thumbnail_url))

        return titles

    else:
        print('\nError from YouTube\'s side.')
        return [(-1, '', '', '')]
