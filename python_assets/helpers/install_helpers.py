import pathlib

import re

from python_assets.tools import sh


def make(make_dir: pathlib.Path, install_dir: pathlib.Path, configure=True, make_install=True, config_prefix=True, install_prefix=True):
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

    for subcommand in commands:
        sh(subcommand, cwd=make_dir)
