import pathlib

from tools import sh


def make(directory: pathlib.Path):
    command = '''
    make
    make install
    '''

    if 'configure' in directory.iterdir():
        command = './configure\n' + command

    sh(command, cwd=directory)

