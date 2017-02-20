import unittest
import pathlib
import tempfile

import python_assets


class TestUnpack(unittest.TestCase):
    gz_file = 'https://codeload.github.com/kennethreitz/requests/zip/v2.13.0'
    tar_gz = "https://codeload.github.com/Ensembl/ensembl-vep/tar.gz/release/87.24"

    def test_extract(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = pathlib.Path(temp_dir)
            python_assets.unpack_into(self.gz_file, path)
            self.assertGreater(len(list(path.iterdir())), 12)

    def test_no_extract(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = pathlib.Path(temp_dir)
            python_assets.unpack_into(self.gz_file, path, extract=False)
            self.assertEqual(len(list(path.iterdir())), 1)

    def test_tar_gz(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = pathlib.Path(temp_dir)
            python_assets.unpack_into(self.tar_gz, path)
            self.assertGreater(len(list(path.iterdir())), 1)
