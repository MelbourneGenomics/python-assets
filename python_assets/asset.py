import shutil
import tempfile
import enum
import typing
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


#
# class AssetStage:
#     """
#     Represents a single part of the installation process: An asset and it stage
#     """
#     stage: Stage
#     asset: Asset
#
#     def __init__(self, asset:Asset, stage: Stage = Stage.INSTALL):
#         self.asset = asset
#         self.stage = stage
#
#
# class Dependency:
#     dependency: AssetStage
#     dependent:
#
#     def __init__(self,
#                  dependent: typing.Union[typing.NamedTuple, AssertionError],
#                  dependency: typing.Union[typing.NamedTuple, AssertionError]):
#
#         if isinstance(dependent, typing.NamedTuple):
#             self.dependent = dependent
#         elif isinstance(dependent, type[Asset]):
#             self.dependent = (dependent, Stage.INSTALL)
#
#         if isinstance(dependency, typing.NamedTuple):
#             self.dependency = dependency
#         elif isinstance(dependency, type[Asset]):
#             self.dependency = (dependency, Stage.INSTALL)


class Asset:
    """
    Base class used for assets. Child classes should implement the download and install methods
    """

    directory: Path

    def __init__(self, directory: Path):
        self.directory = directory

    @property
    def id(self) -> typing.Hashable:
        """
        Any hashable object that can be used to identify the Asset. Can include a version etc
        :return:
        """
        return self.__class__

    @property
    def dependencies(self) -> typing.Iterable[typing.Hashable]:
        """
        Returns a list of IDs of assets that need to be installed before this can run
        :return:
        """
        return []

    def execute(self):
        """
        Runs a full installation for this asset
        """
        # TODO: Link together download and install in the same directory
        self.download()
        self.install()

    def download(self) -> Path:
        """
        Download the asset. This should be a process that remains platform-independent (no compilation etc).
            Must return a path-like object pointing at the asset
        :return:
        """
        pass

    def install(self) -> Path:
        """
        Install the asset. This can be platform dependent.
        :return:
        """
        pass


class VersionedAsset(Asset):
    version: str

    def __init__(self, version: str, **kwargs):
        self.version = version
        super().__init__(**kwargs)

# Stage = enum.Enum('stage', ['DOWNLOAD', 'INSTALL'])
# Dependency = typing.namedtuple(
#     'Dependency',
#     ('asset', typing.Type[Asset]),
#     ('stage', Stage)
# )
