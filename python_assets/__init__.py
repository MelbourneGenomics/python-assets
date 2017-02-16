import os
import tempfile
from pathlib import Path

import re
import requests
import shutil


class AssetError(BaseException):
    pass


def get_response_filename(response: requests.Response) -> str:
    # By default we assume the filename is the same as the URL
    filename = Path(response.url).name

    # However, if it has a Content-Disposition, use that instead
    filename_re = re.compile('(?<=filename=).+')
    disposition = response.headers.get('Content-Disposition')

    if disposition:
        match = filename_re.search(disposition)
        if match:
            filename = match.group(0)

    return filename


class CompressionEvaluation:
    compression: str = None
    archive: str = None

    @property
    def combined(self):
        """
        Returns a combined archive + compression string which is a valid format for shutil.unpack_archive
        """
        if self.archive == 'zip':
            return 'zip'
        elif self.archive == 'tar':
            return self.compression + 'tar'

    def __init__(self, response: requests.Response):

        filename = get_response_filename(response)

        suffixes = Path(filename).suffixes

        if '.tar' in suffixes:
            self.archive = 'tar'
        if '.gz' in suffixes:
            self.compression = 'gz'
        if '.bz2' in suffixes:
            self.compression = 'bz'
        if '.xz' in suffixes:
            self._compression = 'xz'
        if '.zip' in suffixes:
            self.archive = 'zip'


def unpack_into(url: str, path: os.PathLike, extract=True, compression=None, archive=None, move_root=True):
    """
    Unpacks a download into a directory
    :param extract True if we should extract files from their archives (tar files, zip files)
    :param archive The type of archive (e.g. tar, zip)
    :param compression The type of compression the file has (e.g. xz, bz2, or tar)
    :param move_root If true, strips the first component of each filename, so that if the archive contains a root
        directory, this will not be in the final output
    """

    path = Path(path)

    # Create output if not exists
    path.mkdir(parents=True, exist_ok=True)

    # Do the download
    response = requests.get(url, stream=True)

    # Work out what type of compression it has, overriding with user recommendations
    evaluation = CompressionEvaluation(response)
    if compression:
        evaluation.compression = compression
    if archive:
        evaluation.archive = archive

    # Do the extraction
    if extract:

        # Write the download to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_download:
            shutil.copyfileobj(response.raw, temp_download)

        # Unpack the download into the target directory
        shutil.unpack_archive(temp_download.name, str(path), evaluation.combined)

        # Do the move_root (see the docstring above)
        if move_root:
            files = list(path.iterdir())
            if len(files) == 1 and files[0].is_dir():
                lone_dir = files[0]
                for subfile in lone_dir.iterdir():
                    subfile.rename(path / subfile.name)
                lone_dir.rmdir()

    else:
        # If we're not extracting, just copy the file into the target directory
        filename = get_response_filename(response)
        with (path / filename).open('wb') as dest:
            shutil.copyfileobj(response.raw, dest)

