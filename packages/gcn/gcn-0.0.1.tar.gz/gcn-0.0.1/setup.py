#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
import os
# get __version__ from _version.py
ver_file = os.path.join('gcn', '_version.py')

with open(ver_file) as f:
    exec(f.read())

DISTNAME = 'gcn'

INSTALL_REQUIRES = [i.strip() for i in open("requirements.txt").readlines()]

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = __version__

setuptools.setup(
    name='gcn',
    version=VERSION,
    author="Sujit Rokka Chhetri",
    author_email="sujitchhetri@gmail.com",
    description="A Python library for Graph Convolutional Neural Networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sujit-O/gcn.git",
    packages=setuptools.find_packages(exclude=['dataset', 'py-env', 'build', 'dist', 'venv','intermediate','output','gcn.egg-info']),
    package_dir={DISTNAME: 'gcn'},
    setup_requires=['sphinx>=2.1.2'],
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)