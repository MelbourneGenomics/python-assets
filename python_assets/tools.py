import subprocess
import typing
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


def sh_add_outputs(command, return_dict: dict, dict_key: str, **kwargs):
    """
    Runs a command and stores the stderr and stdout from the process in the dictionary in key
    """
    stdout, stderr = sh(command, **kwargs)
    return_dict[dict_key]['stderr'] = stderr
    return_dict[dict_key]['stdout'] = stdout


def sh(command, **kwargs) -> dict:
    """"
    Runs a command as a subprocess. Captures the stdout and stderr and returns them as a tuple
    """

    if isinstance(command, str):
        # If it's a shell command, enable the shell and ensure `set -e`
        kwargs['shell'] = True
        command = 'set -e\n' + command
    else:
        kwargs['shell'] = False

    proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    return {
        'stdout': proc.stdout,
        'stderr': proc.stderr
    }
