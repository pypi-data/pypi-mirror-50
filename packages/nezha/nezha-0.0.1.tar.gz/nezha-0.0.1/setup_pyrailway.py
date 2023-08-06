#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'pycryptodome',
    'requests',
]

setup(
    name='nezha',
    version='0.0.1',
    author='kougazhang',
    author_email='kougazhang@gmail.com',
    url='https://github.com/kougazhang',
    description="pyrailway, pysuway's railway",
    packages=find_packages(include='pyrailway'),
    install_requires=install_requires,
    include_package_data=True
)
