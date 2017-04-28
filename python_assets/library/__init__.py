from pathlib import Path
from multiprocessing.connection import Connection

from python_assets.asset import Asset, VersionedAsset, extract_asset
from python_assets.tools import sh
from python_assets import install_helpers
from python_assets import download_helpers


class Perl5Asset(VersionedAsset):
    @property
    def id(self):
        return 'perl'

    @extract_asset
    def download(self, download_dir: Path, pipe: Connection):
        return download_helpers.http_download(f"http://www.cpan.org/src/5.0/perl-{self.version}.tar.gz", download_dir)

    def install(self, download_dir: Path, pipe: Connection):
        sh(['bash', 'Configure', '-de', f'-Dprefix={self.directory}'], cwd=download_dir)
        install_helpers.make(download_dir, self.directory, configure=False)


class VepAsset(VersionedAsset):
    @property
    def id(self):
        return 'vep'

    @property
    def dependency_ids(self):
        return ['perl']

    def download(self, download_dir: Path, pipe: Connection):
        return download_helpers.http_download(
            f"https://codeload.github.com/Ensembl/ensembl-vep/tar.gz/release/{self.version}", download_dir)

    def install(self, download_dir: Path, pipe: Connection):
        for file in download_dir.iterdir():
            file.rename(self.directory / file.name)
