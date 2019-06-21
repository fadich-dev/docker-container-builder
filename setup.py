from typing import Union, Generator
from setuptools import setup, find_packages


def read_file(f: str, by_line: bool = False) -> Union[str, Generator]:
    with open(f) as file:
        if by_line:
            return (line.strip() for line in file.readlines())
        return file.read()


setup(
    name='container_builder',
    description='Builder for Docker containers',
    version='0.1.0',
    packages=find_packages(),
    install_requires=read_file('requirements.txt', by_line=False),
    entry_points={
        'console_scripts': [
            'dcb = container_builder.build:main',
            'container-builder = container_builder.build:main',
        ],
    }
)
