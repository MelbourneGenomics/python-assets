import urllib.request
import pathlib
import os
import wget


def http_download(url, dir):
    # local_filename, headers = urllib.request.urlretrieve(url)
    # return pathlib.Path(local_filename)
    dir = os.fspath(dir)
    return pathlib.Path(wget.download(url, dir))
