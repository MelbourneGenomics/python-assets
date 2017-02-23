from setuptools import setup, find_packages

setup(
    name="python_assets",
    version="0.0.1",
    packages=find_packages(),
    test_suite="test",
    install_requires=[
        'requests',
        'networkx'
    ],
    license="GPL"
)
