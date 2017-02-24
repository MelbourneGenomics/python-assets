import subprocess
from pathlib import Path


def move_root(path: Path):
    """
    Strips the first component of each filename, so that if the archive contains a root directory, this will not be in
        the final output
    :param path:
    :return:
    """
    files = list(path.iterdir())
    if len(files) == 1 and files[0].is_dir():
        lone_dir = files[0]
        for subfile in lone_dir.iterdir():
            subfile.rename(path / subfile.name)
        lone_dir.rmdir()


def sh(command, **kwargs):
    if isinstance(command, str):
        # If it's a shell command, enable the shell and ensure `set -e`
        kwargs['shell'] = True
        command = 'set -e\n' + command
    else:
        kwargs['shell'] = False

    subprocess.check_call(command, **kwargs)
