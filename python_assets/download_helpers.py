import urllib.request
import pathlib


def http_download(url):
    local_filename, headers = urllib.request.urlretrieve(url)
    return pathlib.Path(local_filename)