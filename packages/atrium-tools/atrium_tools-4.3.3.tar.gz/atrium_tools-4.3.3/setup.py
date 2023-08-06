#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce logiciel est régi par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"

import setuptools

from nuxeolib import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Application name:
    name="atrium_tools",

    # Version number (initial):
    version=version.__version__,

    # Application author details:
    author="Chris Arnault",
    author_email="arnault@lal.in2p3.fr",
    description="Atrium utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Packages

    packages=["atrium_shell", "nuxeolib"],

    # Include additional files into the package
    # include_package_data=True,

    # Details
    url="https://atrium.in2p3.fr/",

    #
    # license="LICENSE.txt",

    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
    ],
)

