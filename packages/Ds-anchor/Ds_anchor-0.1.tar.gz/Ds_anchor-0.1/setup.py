#!/usr/bin/env python
from setuptools import setup
from setuptools import setup, find_packages
setup(name='Ds_anchor',
    version='0.1',
    description='A explainer that uses anchor to exaplin black box model',
    author='Nai JunWang, JingZhi Ju',
    author_email='805812404@qq.com',
    url='https://github.com/alexwong1995/DsRule',
    packages=find_packages(),
    platforms=["all"],
)