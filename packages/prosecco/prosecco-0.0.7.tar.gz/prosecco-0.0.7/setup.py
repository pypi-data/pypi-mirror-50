#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from glob import glob
import prosecco

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prosecco",
    version=prosecco.__version__,
    author="Michal Szczepanski",
    author_email="michal@vane.pl",
    description="Simple, extendable nlp engine that can extract data based on provided conditions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/vane/prosecco",
    packages=setuptools.find_packages(),
    package_data={
        'prosecco': [
            'example/advanced.py',
            'example/basic.py',
            'example/custom_condition_class.py',
            'example/qa.py',
            'example/superhero.txt',
            'data/en/suffix.txt',
            'data/pl/bye.txt',
            'data/pl/hi.txt',
            'data/pl/prefix.txt',
            'data/pl/preposition.txt',
            'data/pl/pronoun.txt',
            'data/pl/stopwords.txt',
            'data/pl/suffix.txt',
            'data/pl/swear.txt',
            'data/pl/thx.txt',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
