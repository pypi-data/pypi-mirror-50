#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import sys

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'click>=6.0'
]

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup_requirements = [
    #'pytest-runner'
] + pytest_runner

test_requirements = [
    'pytest',
    'coverage',
    'flake8'
]




setup(
    author="Thorsten Beier",
    author_email='derthorstenbeier@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="py_tools is a modern python library",
    entry_points={
        'console_scripts': [
            'py_tools=py_tools.cli.main:cli',
        ],
    },
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='py_tools',
    name='my-py-tools',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DerThorsten/py_tools',
    version='0.1.11',
    zip_safe=False,
)
