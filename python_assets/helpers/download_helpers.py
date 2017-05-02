import urllib.request
import pathlib
import os
import wget


def http_download(url, dir):
    dir = os.fspath(dir)
    return pathlib.Path(wget.download(url, dir, bar=None))
