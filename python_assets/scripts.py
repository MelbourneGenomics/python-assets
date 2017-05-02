"""Contains the entry point/executable scripts from the library"""
import importlib
from python_assets.core.bundle import Bundle
import os
from pathlib import Path
import argparse


def asset_bundle(assetfile: Path):
    spec = importlib.util.spec_from_file_location("assetfile", assetfile)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    bundle = module.bundle

    if not isinstance(bundle, Bundle):
        raise 'The bundle exposed in the assetfile must be an instance of the Bundle class'

    return bundle


def directory_path(input):
    path = Path(input)
    if path.is_file():
        raise argparse.ArgumentTypeError(f'{input} is the path to an existing file; it must be a directory')
    else:
        return path


def file_path(input):
    path = Path(input)
    if path.is_file():
        return path
    else:
        raise argparse.ArgumentTypeError(f'{input} must be the path to an existing file')


def main():
    # Import the assetfile from the current directory
    here = Path(os.getcwd())

    # Parse args
    parser = argparse.ArgumentParser(description='Installs assets needed by the python application')
    parser.add_argument('-d', '--dir', help='Root directory into which the assets will be installed',
                        type=directory_path, default=here, required=False)
    parser.add_argument('-a', '--assetfile',
                        help='Path to the assetfile to use to determine which assets to install',
                        type=file_path, required=False)
    parser.set_defaults(command='install')
    subparsers = parser.add_subparsers(dest='command')

    # Install parser
    install_parser: argparse.ArgumentParser = subparsers.add_parser('install', help='Install the asset bundle')

    # List parser
    list_parser: argparse.ArgumentParser = subparsers.add_parser('list', help='List the assets in the asset bundle')

    # Do the parsing
    args = parser.parse_args()

    # Process some args
    if args.assetfile is None:
        args.assetfile = args.dir / 'assetfile.py'

    # Load the bundle
    bundle = asset_bundle(args.assetfile)
    if args.dir is not None:
        bundle.directory = args.dir

    # Execute the commands
    if args.command == 'install' or args.command is None:
        bundle.install()
    elif args.command == 'list':
        bundle.list()
