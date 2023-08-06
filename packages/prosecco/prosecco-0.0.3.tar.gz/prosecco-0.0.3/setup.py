#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

import prosecco

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prosecco",
    version=prosecco.__version__,
    author="Michal Szczepanski",
    author_email="michal@vane.pl",
    description="Slim, flexible and extendable NLP engine that can produce list of features from text based on provided condtions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/vane/prosecco",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
    ],
)
