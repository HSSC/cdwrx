#!/usr/bin/env python

from setuptools import setup

setup (
    setup_requires=['pbr'],
    pbr=True,
    package_dir={ 'cdwrx':'src' },
    packages=['cdwrx' ],
    test_suite='test'
)
