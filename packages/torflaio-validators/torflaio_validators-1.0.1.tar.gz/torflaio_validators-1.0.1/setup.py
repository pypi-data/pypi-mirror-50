#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='torflaio_validators',
    version='1.0.1',
    description='Tornado, Flask, AioHttp params validators',
    author='yirantai',
    author_email='896275756@qq.com',
    license='BSD License',
    packages=find_packages(),
    url='https://github.com/yirantai/torflaio_validators.git',
    install_requires=[
        'python-dateutil>=2.8.0'
    ]
)