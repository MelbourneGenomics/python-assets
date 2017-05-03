import typing
import re
from typing import NamedTuple


class Version():
    """Represents a version of an asset, for use in dependencies"""

    def __init__(self, *args):
        self.increments = args

    def __str__(self):
        return '.'.join([str(i) for i in self.increments])

    increments: typing.Iterable
    """An array of versions, e.g. a version 1.2.1 might be [1, 2, 1]"""


class Dependency(NamedTuple):
    """Represents a dependency an asset may have, including version constraints"""

    id: str
    """The string identifier of the asset"""

    exact_version: Version
    """The exact version the asset must have"""

    min_version: Version
    """The minimum version the asset must have"""

    max_version: Version
    """The maximum version the asset must have"""

    # def __init__(self, id: str, exact_version: Version = None, min_version: Version = None,
    #              max_version: Version = None):
    #     self.id = id
    #     self.exact_version = exact_version
    #     self.min_version = min_version
    #     self.max_version = max_version


class Provision(NamedTuple):
    """A dependency that an asset provides"""
    id: str
    version: Version

    @staticmethod
    def parse(raw: str):
        re.search(r'\w')
