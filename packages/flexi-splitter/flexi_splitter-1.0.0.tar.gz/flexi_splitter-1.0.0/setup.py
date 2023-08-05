#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flexi_splitter",
    version="1.0.0",
    packages=['flexi_splitter'],
    install_requires=[
        'biopython',
        'pyyaml'
    ],
    author="Laurent Modolo, Emmanuel, Labaronne",
    author_email="laurent.modolo@ens-lyon.fr",
    description="Sort reads into different fastq files from a barcode list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LBMC/rmi_splitter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, \
version 2.1 (CeCILL-2.1)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['flexi_splitter=flexi_splitter.flexi_splitter:main'],
    }
)
