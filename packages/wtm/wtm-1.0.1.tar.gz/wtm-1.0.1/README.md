# wtm - what the music

A song downloader for your command line. Enter keywords for songs and `wtm` will scrape the internet for you and download the appropriate song.

## Installation

Install globally using `pip`. You might have to use `sudo`.

```bash
$ pip install wtm
```

## Usage

```shell
$ wtm --help
usage: wtm [-h] [-s SONG [SONG ...]] [-t] [-v]

Downloads songs from the internet.

optional arguments:
  -h, --help          show this help message and exit
  -s SONG [SONG ...]  song search query
  -t, --top           selects top search result
  -v, --version       show program's version number and exit
```

To enter keywords, either enter directly from the command line using the `-s` flag or you'll be prompted to enter the query.

If you trust YouTube with your query, you can pass the `-t` flag to get the first top result. Or else you'll be asked to select
an id from a list of the titles that wtm scraped. Please see the demo for more information.

# Demo

[![asciicast](https://asciinema.org/a/259737.svg)](https://asciinema.org/a/259737)
