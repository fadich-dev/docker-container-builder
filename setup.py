import os

from typing import Union, Generator
from setuptools import setup, find_packages

WOR_DIR = os.path.dirname(os.path.abspath(__file__))


def read_file(f: str, by_line: bool = False) -> Union[str, Generator]:
    with open(f) as file:
        if by_line:
            return (line.strip() for line in file.readlines())
        return file.read()


setup(
    name='container_builder',
    description='Builder for Docker containers',
    version='0.1.1',
    packages=find_packages(),
    install_requires=read_file(os.path.join(WOR_DIR, 'requirements.txt'), by_line=False),
    entry_points={
        'console_scripts': [
            'dcb = container_builder.build:main',
            'container-builder = container_builder.build:main',
        ],
    }
)
