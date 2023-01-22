#!/usr/bin/env python
import logging
import os

from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

logger = logging.getLogger(__name__)

setup(
    name='pyopstools',
    version='0.1.0',
    author='George Benjamin-Schonberger',
    author_email='<george.benjamin@gmail.com>',
    description='DevOps CLI tools',
    keywords=['ops', 'api', 'tester', 'tools'],
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/adeotek/pyopstools',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires = '>=3.7',
    install_requires=[
        "colorama",
        "termcolor",
        'requests',
        'click'
    ],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'pyopstools = main:cli',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT",
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Opera,ting System :: Microsoft :: Windows',
    ]
)
