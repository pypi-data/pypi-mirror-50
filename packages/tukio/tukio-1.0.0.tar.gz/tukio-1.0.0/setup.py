#!/usr/bin/env python
from setuptools import setup, find_packages


try:
    with open('VERSION.txt', 'r') as v:
        version = v.read().strip()
except FileNotFoundError:
    version = '0.0.0.dev0'

with open('DESCRIPTION', 'r') as d:
    long_description = d.read()

setup(
    name='tukio',
    description='An event-based workflow library built around asyncio',
    long_description=long_description,
    url='https://github.com/surycat/tukio',
    author='Enovacom Surycat',
    author_email='rand@surycat.com',
    version=version,
    packages=find_packages(exclude=['tests']),
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
