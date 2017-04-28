import pathlib
import tempfile

import multiprocessing
import multiprocessing.connection

import subprocess
import time
import datetime
import shutil

from python_assets.core import asset

class TimeInterval:
    """Represents the difference between two datetimes"""
    start: datetime.datetime
    finish: datetime.datetime

    def __init__(self, start, finish):
        self.start = start
        self.finish = finish


class GraphAsset(asset.Asset):
    """A dummy asset that doesn't actually install anything, that can be used to test asset install order"""

    def __init__(self):
        super().__init__(tempfile.mkdtemp())

    def install(self, download_dir, return_dict: dict):

        # Time when this starts and finishes, and send that
        start = datetime.datetime.now()
        time.sleep(1)
        finish = datetime.datetime.now()

        return_dict['time'] = TimeInterval(start, finish)

    def is_overlap(self, b: 'GraphAsset'):
        """Returns True if this asset overlapped in execution time with another asset"""

        # Take all permutations of the tuples
        for a, b in [[self, b], [b, self]]:

            # Take all points in tuple A
            for point in [a.piped['time'].start, a.piped['time'].finish]:

                # If that point is within B, there is overlap
                if b.piped['time'].start <= point <= b.piped['time'].finish:
                    return True

        return False


class GzipAsset(asset.Asset):
    """A dummy asset that copies the 'gzip' executable from /bin to the directory"""

    def __init__(self):
        super().__init__(pathlib.Path('bin'))

    @property
    def id(self):
        return 'gzip'

    def download(self, download_dir: pathlib.Path, pipe: multiprocessing.connection.Connection):
        """Emulate a download by copying the tar executable from the system"""
        tar = subprocess.check_output('which gzip', shell=True, executable='/bin/bash').decode().strip()
        shutil.copy(tar, download_dir)

    def install(self, download_dir: pathlib.Path, pipe: multiprocessing.connection.Connection):
        shutil.copy(download_dir / 'gzip', self.directory)


class TarAsset(asset.Asset):
    """A dummy asset that copies the 'tar' executable from /bin to the directory"""

    def __init__(self):
        super().__init__(pathlib.Path('bin'))

    @property
    def dependency_ids(self):
        return ['gzip']

    def download(self, download_dir: pathlib.Path, pipe: multiprocessing.connection.Connection):
        """Emulate a download by copying the tar executable from the system"""
        tar = subprocess.check_output('which tar', shell=True, executable='/bin/bash').decode().strip()
        shutil.copy(tar, download_dir)

    def install(self, download_dir: pathlib.Path, pipe: multiprocessing.connection.Connection):
        shutil.copy(download_dir / 'tar', self.directory)
