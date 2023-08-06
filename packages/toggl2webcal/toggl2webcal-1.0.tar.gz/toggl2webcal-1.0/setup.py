#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='toggl2webcal',
    version='1.0',

    description="Export toggl to webcal file - uses sql database to store toggl data to get around API limits ",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Visgean",
    author_email='visgean@gmail.com',
    url='https://github.com/visgean/toggl2webcal',
    packages=[
        'toggl2webcal',
    ],
    package_dir={'toggl2webcal': 'toggl2webcal'},
    license="MIT",
    keywords='toggl webcal',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'argparse',
        'requests',
        'icalendar',
        'python-dateutil',
        'sqlalchemy',
    ],
    entry_points={
        'console_scripts': [
            'toggl2webcal = toggl2webcal.main:main'
        ]
    },
)
