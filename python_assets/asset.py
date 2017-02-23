import shutil
import tempfile
from pathlib import Path

from tools import move_root


def extract_asset(download_func, strip_root=True):
    """
    Decorator to indicate that an asset should be extracted
    :return:
    """

    def replacement(directory: Path):
        # First do the download, but download to a temp dir
        with tempfile.TemporaryDirectory as temp_dir:
            asset = download_func(temp_dir)

            # Then extract
            shutil.unpack_archive(asset, directory)

            if strip_root:
                move_root(directory)

    return replacement


class Asset:
    """
    Base class used for assets. Child classes should implement the download and install methods
    """

    directory: Path


    @property
    def dependencies(self):
        """
        Returns a list of other Asset classes that need to be installed before this can run
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def download():
        """
        Download the asset. This should be a process that remains platform-independent (no compilation etc).
            Must return a path-like object pointing at the asset
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def install():
        """
        Install the asset. This can be platform dependent.
        :return:
        """
        raise NotImplementedError()
