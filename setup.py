from setuptools import setup, find_packages

setup(
    name="python_assets",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'pyasset = python_assets.scripts:main'
        ]
    },
    packages=find_packages(),
    test_suite="test",
    install_requires=[
        'progress',
        'requests',
        'networkx',
        'wget'
    ],
    license="GPL"
)
