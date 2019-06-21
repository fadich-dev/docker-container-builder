import os

from setuptools import setup, find_packages

WOR_DIR = os.path.dirname(os.path.abspath(__file__))

setup(
    name='container_builder',
    description='Builder for Docker containers',
    version='0.1.4',
    packages=find_packages(),
    install_requires=(
        'argh==0.26.2',
        'docker==4.0.2',
    ),
    entry_points={
        'console_scripts': [
            'dcb = container_builder.build:main',
            'container-builder = container_builder.build:main',
        ],
    }
)
