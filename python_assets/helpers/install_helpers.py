import pathlib

import re

from python_assets.tools import sh


def make(make_dir: pathlib.Path, install_dir: pathlib.Path, configure=True, make_install=True, config_prefix=True, install_prefix=True):
    """
    Runs configure, make, and make install on the directory provided
    :param make_dir: The directory containing the source code, in which to run make
    :param install_dir: The directory in which to make install. e.g. /usr
    :param configure: True if we want to run the configure script
    :param make_install: True if we want to run make install
    :param config_prefix: True if we want to run configure with the prefix of the install directory
    :param install_prefix: True if we want to run make install with the prefix of the install director
    :return:
    """
    commands = [['make']]

    # Add make install if needed
    if make_install:
        install_cmd = ['make', 'install']
        if install_prefix:
            install_cmd.append(f'prefix={install_dir}')
        commands.append(install_cmd)

    # Add configure line if needed
    if configure:
        for path in make_dir.iterdir():
            match = re.search('configure$', str(path), re.IGNORECASE)
            if match:
                config_cmd = ['sh', str(path)]
                if config_prefix:
                    config_cmd.append(f'--prefix={install_dir}')
                commands.insert(0, config_cmd)
                break

    outputs = []
    for subcommand in commands:
        outputs.append(sh(subcommand, cwd=make_dir))

    return outputs
