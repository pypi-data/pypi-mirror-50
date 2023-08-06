#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
 

setup(
    name="oudjirasign",
    version="0.1",
    description="Module python de signature electronique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/oumar90/oudjirasign",
    author="Oumar Djimé Ratou",
    author_email="oudjira90@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["oudjirasign"],
    include_package_data=True,
    install_requires=["pycryptodome","progress", "cryptography", "argparse"],
    entry_points={
        "console_scripts": [
            "oudjirasign=oudjirasign:main",
        ]
    },
)