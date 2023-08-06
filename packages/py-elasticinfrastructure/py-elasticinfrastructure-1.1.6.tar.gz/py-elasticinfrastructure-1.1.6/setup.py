import os
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='py-elasticinfrastructure',
    version='1.1.6',
    description='A small utilty to index infrastructure metrics to elasticsearch',
    author='NullConvergence',
    packages=find_packages(),
    install_requires=required
)
