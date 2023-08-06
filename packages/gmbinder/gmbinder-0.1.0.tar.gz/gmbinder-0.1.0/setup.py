#!/usr/bin/env python3
from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='gmbinder',
    version='0.1.0',
    description='Python binding of gmbinder API and cli tool',
    license="GPLv3",
    long_description=long_description,
    author='Tristan Sweeney',
    author_email='sweeney.tr@husky.neu.edu',
    url="http://www.foopackage.com/",
    packages=['gmbinder'],  #same as name
    install_requires=['requests'], #external packages as dependencies
    extras_require = {
            'PDF': ['selenium', 'browsermob-proxy'],
    },
    entry_points={
            'console_scripts': [
                    'gmcli = gmbinder.cli:cli'
            ]
    },
)