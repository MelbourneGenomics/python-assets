import os
import typing
from pathlib import Path
from multiprocessing.connection import Connection
import requirements

from python_assets.core.asset import VersionedAsset, extract_asset, NamedAsset, Asset
from python_assets.tools import sh
from python_assets.helpers import install_helpers, download_helpers


class Perl5Asset(VersionedAsset):
    @property
    def id(self):
        return 'perl'

    @extract_asset
    def download(self, download_dir: Path, return_dict: dict):
        return download_helpers.http_download(f"http://www.cpan.org/src/5.0/perl-{self.version}.tar.gz", download_dir)

    def install(self, download_dir: Path, return_dict: dict):
        return_dict['configure'] = sh(['bash', 'Configure', '-de', f'-Dprefix={self.directory}'], return_dict,
                                      'install_', cwd=download_dir)
        return_dict['install'] = install_helpers.make(download_dir, self.directory, configure=False)


class Python2Asset(VersionedAsset):
    @property
    def id(self):
        return 'python2'

    @extract_asset
    def download(self, download_dir: Path, return_dict: dict):
        return download_helpers.http_download(
            f"https://www.python.org/ftp/python/{self.version}/Python-{self.version}.tgz", download_dir)

    def install(self, download_dir: Path, return_dict: dict):
        return_dict['install'] = install_helpers.make(download_dir, self.directory)

    @property
    def is_complete(self):
        return (self.bundle.directory / 'bin/python2').exists()


class PipAssetBundle(Asset):

    packages: set

    """
    Represents an set of pip packages as a single asset, since they can more efficiently be installed together
    """
    def __init__(self, packages: typing.Union[os.PathLike, typing.List[str]]):

        if isinstance(packages, os.PathLike) and os.path.exists(packages):
            self.packages = set()
            with packages.open('r') as f:
                for line in f:
                    self.packages.append(line)
        elif isinstance(packages, typing.List):
            self.packages = set(packages)

        super().__init__()

    @property
    def packages_fmt(self):
        return ' '.join([f"'{dep}'" for dep in self.packages])

    def download(self, download_dir: Path, return_dict: dict):
        return_dict['download'] = sh(f'python2 -m pip download -d {download_dir} --no-binary :all: {self.packages_fmt}')

    def install(self, download_dir: Path, return_dict: dict):
        return_dict['install'] = sh(f'python2 -m pip install --no-index --find-links={download_dir} {self.packages_fmt}')

    @property
    def is_complete(self):
        deps = requirements.parse(sh('python2 -m pip freeze')['stdout'].decode())
        dep_names = set([dep.name for dep in deps])
        return self.packages.issubset(dep_names)

class SamtoolsAsset(VersionedAsset):
    @extract_asset
    def download(self, download_dir: Path, return_dict: dict):
        return download_helpers.http_download(
            f"https://github.com/samtools/samtools/releases/download/{self.version}/samtools-{self.version}.tar.bz2",
            download_dir)

    def install(self, download_dir: Path, return_dict: dict):
        return_dict['install'] = install_helpers.make(download_dir, self.directory)

    @property
    def is_complete(self):
        return (self.bundle.directory / 'bin/samtools').exists()


class VepAsset(VersionedAsset):
    @property
    def id(self):
        return 'vep'

    @property
    def requires(self):
        return ['perl']

    def download(self, download_dir: Path, pipe: Connection):
        return download_helpers.http_download(
            f"https://codeload.github.com/Ensembl/ensembl-vep/tar.gz/release/{self.version}", download_dir)

    def install(self, download_dir: Path, pipe: Connection):
        for file in download_dir.iterdir():
            file.rename(self.directory / file.name)
