import os
import shutil
import tempfile
import typing
from pathlib import Path

import multiprocessing
import multiprocessing.connection

import python_assets.tools
import python_assets.core.bundle

def extract_asset(download_func, strip_root=True):
    """
    Decorator to indicate that an asset should be extracted
    :return:
    """

    def replacement(self, directory: Path, pipe: multiprocessing.connection.Connection):
        # First do the download, but download to a temp dir
        with tempfile.TemporaryDirectory() as temp_dir:
            asset = download_func(self, temp_dir, pipe)

            # Then extract
            shutil.unpack_archive(str(asset), directory)

            if strip_root:
                python_assets.tools.move_root(directory)

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

    dependencies: int
    """Count of assets that this asset depends on. This will be automatically populated by the installer"""

    dependents: list
    """List of assets that depend on this asset. This will be automatically populated by the installer"""

    _directory: Path
    """The relative path to the installation directory for the asset, from the bundle root. Use .directory for
    the absolute path. If a default value is set for this, it should be a path using a unix filesystem, e.g.
    /usr/bin/"""

    visited: bool
    """Whether we've visited this node so far in topographical sort"""

    piped: typing.Any
    """Arbitrary data that was returned from the process"""

    bundle: 'python_assets.bundle.Bundle'
    """The parent bundle"""

    def __init__(self, directory: os.PathLike = None):
        self._directory = Path(directory)
        self.dependencies = 0
        self.dependents = []
        self.piped = None
        self.visited = False

    @property
    def directory(self):
        """The absolute path to the folder this asset will install into"""
        return (self.bundle.directory / self._directory).resolve()

    def dependency_completed(self):
        """
        Called when a dependency of this is completed. e.g. if there is a dependency A → self, and A was just completed
        self.dependency_completed() will be called.
        :return:
        """
        self.dependencies -= 1

    def add_dependent(self, asset: 'Asset'):
        """
        Establishes an edge in the dependency graph from self → asset. Not that this is the opposite of how you might
        expect, it does NOT establish a dependency from asset → self!
        :param asset:
        :return:
        """
        self.dependents.append(asset)
        asset.dependencies += 1

    def complete(self):
        """
        Called when this asset has finished installing. Updates all dependents
        :return:
        """
        for dependent in self.dependents:
            dependent.dependency_completed()

    @property
    def deps_satisfied(self):
        """
        Returns true if all the dependencies are satisfied
        :return:
        """
        return self.dependencies == 0

    @property
    def id(self) -> typing.Hashable:
        """
        Any hashable object that can be used to identify the Asset. Can include a version etc
        :return:
        """
        return self.__class__

    @property
    def dependency_ids(self) -> typing.Iterable[typing.Hashable]:
        """
        Returns a list of IDs of assets that need to be installed before this can run
        :return:
        """
        return []

    def execute(self, pipe: multiprocessing.connection.Connection):
        """
        Runs a full installation for this asset
        """
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            return_dict = {}
            self.directory.mkdir(exist_ok=True, parents=True)
            self.download(temp_path, return_dict)
            self.install(temp_path, return_dict)

            pipe.send(return_dict)

    def download(self, download_dir: Path, return_dict: dict):
        """
        Download the asset. This should be a process that remains platform-independent (no compilation etc).
            Should return the path to the asset itself (which will be inside the download_dir)
        :return:
        """
        pass

    def install(self, download_dir: Path, return_dict: dict):
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
