#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

# Package meta-data.
NAME = 'genetic_optimizer'
DESCRIPTION = 'Genetic algorithm optimizer using K-Means clustering with one way ANOVA algorithms.'
URL = 'https://github.com/szachovy/GeneticOptimizer'
EMAIL = 'wjmaj98@gmail.com'
AUTHOR = 'WJ Maj'
REQUIRES_PYTHON = '>=3.6.5'
VERSION = '0.1'

REQUIRED = [
    'configparser>=3.7.4',
    'numpy>=1.16.3',
    'pandas>=0.24.2',
    'xlsxwriter>=1.1.8',
    'sklearn>=0.0',
    'scipy>=1.3.0',
    'matplotlib>=3.1.0'
]

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name=NAME,
    version=VERSION,

    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type='text/markdown',

    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,

    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)