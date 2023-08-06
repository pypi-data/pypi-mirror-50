#!/usr/bin/env python3
"""
Pixel Art Fx

:copyright: 2015 Aurélien Gâteau.
:license: Apache 2.0.
"""
from setuptools import setup

import pafx

DESCRIPTION = 'Pixel Art effects'


setup(name=pafx.__appname__,
    version=pafx.__version__,
    description=DESCRIPTION,
    author='Aurélien Gâteau',
    author_email='mail@agateau.com',
    license=pafx.__license__,
    platforms=['any'],
    url='http://github.com/agateau/pafx',
    install_requires=[
        'pillow',
    ],
    packages=['pafx'],
)
