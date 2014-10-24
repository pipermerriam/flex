#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

version = "1.5.0"

readme = open(os.path.join(DIR, 'README.md')).read()


setup(
    name='flex',
    version=version,
    description="""Swagger Schema validation.""",
    long_description=readme,
    author='Piper Merriam',
    author_email='pipermerriam@gmail.com',
    url='https://github.com/pipermerriam/flex',
    include_package_data=True,
    py_modules=['flex'],
    install_requires=[
        'drf-compound-fields==0.2.2',
        'Django==1.7',
        'djangorestframework==2.4.3',
        'six==1.7.3',
        'PyYAML==3.11',
        'iso8601==0.1.10',
    ],
    license="BSD",
    zip_safe=False,
    keywords='rest swagger',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
