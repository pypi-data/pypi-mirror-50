#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__name__ = 'monkey.google.api'
__version__ = "0.0.1.dev1"
__author__ = 'Xavier ROY'
__author_email__ = 'xavier@regbuddy.eu'

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://bitbucket.org/monkeytechnologies/monkey-google-api/',
    description='Helper classes for Google API..',
    long_description=open('README.rst').read(),
    license="Apache License, Version 2.0",

    packages=find_packages(),
    include_package_data=True,
    install_requires=['pymongo >= 3.6'],

    # See: https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers'
    ]
)
