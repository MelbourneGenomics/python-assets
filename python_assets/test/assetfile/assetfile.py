import pathlib
import tempfile

from python_assets import bundle, test

here = pathlib.Path(__file__).parent.resolve()

bundle = bundle.Bundle(tempfile.mkdtemp(), [
    test.TarAsset(),
    test.GzipAsset()
])
