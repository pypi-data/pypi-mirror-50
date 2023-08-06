# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

setup(
    name='broker_client',
    version='1.0.0',
    description='A client for the Swarm Broker written in Python',
    author='Geovane Fedrecheski',
    packages=find_packages(exclude=('tests', 'docs'))
)

print(find_packages())
