#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='lens_yaml',
    author='Veit Heller',
    version='0.0.1',
    license='MIT',
    url='https://github.com/port-zero/lens_yaml',
    download_url = 'https://github.com/port-zero/lens_yaml/tarball/0.0.1',
    description='A YAML parser for lens',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('.'),
    install_requires=[
        "pygments",
        "lens-cli",
        "pyyaml",
    ],
)

