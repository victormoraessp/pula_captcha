#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='pula_captcha',
    version='3.5',
    license='open-source',
    author='Victor Pereira',
    author_email='victorthmoraes@gmail.com',
    url='https://github.com/victormoraessp/pula_captcha',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'pula_captcha': ['body.xml']},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests==2.30.0',2]
)
