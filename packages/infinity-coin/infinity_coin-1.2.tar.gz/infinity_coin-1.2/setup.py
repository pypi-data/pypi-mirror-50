#!/usr/bin/env python
# -*- coding: utf-8 -*-
from io import open
from setuptools import setup

"""
:authors: MrSmitix
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2019 MrSmitix
"""


version='1.2'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='infinity_coin',
    version=version,

    author='MrSmitix',
    author_email='mr.smitix@gmail.com',

    description=(
        u'infinity_coin - это python модуль для работы с монетой '
        u'Infinity Сoin (Infinity Сoin API wrapper)'
    ),
    
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/MrSmitix/infinity_coin',
    download_url=f'https://github.com/MrSmitix/infinity_coin/archive/v{version}.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['infinity_coin'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)