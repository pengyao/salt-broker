#!/usr/bin/env python

from saltbroker.metadata import *
from setuptools import setup, find_packages

REQUIREMENTS = [
    'pyzmq>=2.2.0',
    'salt>=2014.1.0',
    'setproctitle'
]

setup(
    name=NAME,
    description=DESCRIPTION,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENCE,
    url=URL,
    packages=find_packages(exclude=['docs']),
    install_requires=REQUIREMENTS,
    scripts=['scripts/salt-broker']
)