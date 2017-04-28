import pathlib
import tempfile

from python_assets import test
from python_assets.core import bundle

here = pathlib.Path(__file__).parent.resolve()

bundle = bundle.Bundle(here, [
    test.TarAsset(),
    test.GzipAsset()
])
