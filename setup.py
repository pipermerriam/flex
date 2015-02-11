#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from pip.download import PipSession
import os

DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

version = '3.1.0'

readme = open(os.path.join(DIR, 'README.md')).read()

requirements = [
    str(req.req) for req in parse_requirements('requirements.txt', session=PipSession())
]


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
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    entry_points={
        'console_scripts': ["flex=flex.cli:main"],
    },
    keywords='rest swagger',
    packages=find_packages(exclude=["tests", "tests.*"]),
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
