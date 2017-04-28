"""Contains the entry point/executable scripts from the library"""
import importlib
from python_assets.bundle import Bundle
import os
from pathlib import Path

def install_dir(dir: Path):
    spec = importlib.util.spec_from_file_location("assetfile", dir / 'assetfile.py')
    assetfile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(assetfile)

    # Install the bundle
    bundle = assetfile.bundle
    if not isinstance(bundle, Bundle):
        raise 'The bundle exposed in the assetfile must be an instance of the Bundle class'
    bundle.install()


def main():
    # Import the assetfile from the current directory
    here = Path(os.getcwd())

    install_dir(here)
