from asset import Asset, VersionedAsset
import install_helpers
import download_helpers


class Perl5Asset(VersionedAsset):
    @property
    def id(self):
        return 'perl'

    def download(self):
        return download_helpers.http_download(f"http://www.cpan.org/src/5.0/perl-{self.version}.tar.gz")

    def install(self):
        install_helpers.make(self.directory)


class VepAsset(VersionedAsset):
    @property
    def id(self):
        return 'vep'

    @property
    def dependencies(self):
        return ['perl']

    def download(self):
        return download_helpers.http_download(
            f"https://codeload.github.com/Ensembl/ensembl-vep/tar.gz/release/{self.version}")
