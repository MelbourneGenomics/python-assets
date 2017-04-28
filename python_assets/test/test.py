import tempfile
import unittest
import pathlib
from python_assets import bundle, scripts
import datetime

from python_assets.test import GzipAsset, TarAsset, GraphAsset, TimeInterval

here = pathlib.Path(__file__).parent.resolve()


class Overlap(unittest.TestCase):
    params = {'month': 1, 'day': 1}

    def test_is_overlap(self):
        a = GraphAsset()
        a.piped = TimeInterval(
            start=datetime.datetime(year=1, **self.params),
            finish=datetime.datetime(year=10, **self.params)
        )

        b = GraphAsset()
        b.piped = TimeInterval(
            start=datetime.datetime(year=5, **self.params),
            finish=datetime.datetime(year=15, **self.params)
        )

        self.assertTrue(a.is_overlap(b))
        self.assertTrue(b.is_overlap(a))

    def test_no_overlap(self):
        a = GraphAsset()
        a.piped = TimeInterval(
            start=datetime.datetime(year=1, **self.params),
            finish=datetime.datetime(year=10, **self.params)
        )

        b = GraphAsset()
        b.piped = TimeInterval(
            start=datetime.datetime(year=15, **self.params),
            finish=datetime.datetime(year=20, **self.params)
        )

        self.assertFalse(a.is_overlap(b))
        self.assertFalse(b.is_overlap(a))


class TarBundle(unittest.TestCase):
    root = pathlib.Path(tempfile.mkdtemp())
    tar = TarAsset()
    gzip = GzipAsset()

    bundle = bundle.Bundle(root, [
        tar,
        gzip
    ])

    def test_installs(self):
        self.bundle.install()
        self.assertGreater(len(list(self.tar.directory)), 0)
        self.assertGreater(len(list(self.gzip.directory)), 0)


class AssetFile(unittest.TestCase):
    def test_install(self):
        scripts.install_dir(here / 'assetfile')


class Graph(unittest.TestCase):
    class A(GraphAsset):
        def __init__(self):
            super().__init__()

        @property
        def id(self):
            return 'a'

    class B(GraphAsset):
        def __init__(self):
            super().__init__()

        @property
        def id(self):
            return 'b'

    class C(GraphAsset):
        def __init__(self):
            super().__init__()

        @property
        def id(self):
            return 'c'

        @property
        def dependency_ids(self):
            return ['a']

    class D(GraphAsset):
        def __init__(self):
            super().__init__()

        @property
        def id(self):
            return 'd'

        @property
        def dependency_ids(self):
            return ['c', 'b']

    def test_graph(self):
        # "Install" the assets
        a = self.A()
        b = self.B()
        c = self.C()
        d = self.D()

        bun = bundle.Bundle([
            a,
            b,
            c,
            d
        ])

        bun.install()

        # A and B should run first
        self.assertTrue(a.is_overlap(b))

        self.assertFalse(a.is_overlap(c))
        self.assertFalse(a.is_overlap(d))

        self.assertFalse(b.is_overlap(c))
        self.assertFalse(b.is_overlap(d))

# class TestUnpack(unittest.TestCase):
#     gz_file = 'https://codeload.github.com/kennethreitz/requests/zip/v2.13.0'
#     tar_gz = "https://codeload.github.com/Ensembl/ensembl-vep/tar.gz/release/87.24"
#
#     def test_extract(self):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             path = pathlib.Path(temp_dir)
#             python_assets.unpack_into(self.gz_file, path)
#             self.assertGreater(len(list(path.iterdir())), 12)
#
#     def test_no_extract(self):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             path = pathlib.Path(temp_dir)
#             python_assets.unpack_into(self.gz_file, path, extract=False)
#             self.assertEqual(len(list(path.iterdir())), 1)
#
#     def test_tar_gz(self):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             path = pathlib.Path(temp_dir)
#             python_assets.unpack_into(self.tar_gz, path)
#             self.assertGreater(len(list(path.iterdir())), 1)
