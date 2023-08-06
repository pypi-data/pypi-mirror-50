# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'celery',
    'jsonschema',
    'nezha',
    'muzha',
    'pandas',
    'pymongo',
    'redis',
    'flower',
    # xinyan
    'M2Crypto'
]

setup(
    name='blueCup',
    version='0.0.12',
    author='kougazhang',
    author_email='kougazhang@gmail.com',
    url='https://github.com/kougazhang',
    description="Little blue cup, who do not love?",
    packages=find_packages(),
    install_requires=install_requires,
)
