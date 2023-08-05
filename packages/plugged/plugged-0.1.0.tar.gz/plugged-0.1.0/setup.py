#!/usr/bin/env python3


from setuptools import setup


VERSION = '0.1.0'
REQUIREMENTS = 'requirements.txt'


def parse_file(path):
    with open(path, 'r') as f:
        req = f.read().split('\n')
    return req


setup(
    name='plugged',
    version=VERSION,
    description='A lightweight arbitrary plugin system based off SourceFileLoaderc',
    license='MIT',
    packages=['plugged'],
    zip_safe=True,
    include_package_data=True,
    # install_requires=parse_file(REQUIREMENTS),
)
