import os
import typing
from pathlib import Path
from multiprocessing.connection import Connection

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
    def __init__(self, packages: typing.Union[Path, typing.Iterable[str]], directory: Path):
        self.dep_arr = []

        if os.path.exists(packages):
            with packages.open('r') as f:
                for line in f:
                    self.dep_arr.append(line)
        elif isinstance(packages, typing.List):
            self.dep_arr = packages

        super().__init__(directory)

    def download(self, download_dir: Path, return_dict: dict):
        return_dict['download'] = sh(f'pip download -d {download_dir}, --no-binary')

    def install(self, download_dir: Path, return_dict: dict):
        return_dict['install'] = sh(f'pip install --no-index --find-links={download_dir} {dep}')


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
