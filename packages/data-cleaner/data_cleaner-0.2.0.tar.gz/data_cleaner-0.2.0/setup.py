#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Archivo de instalación

Para deployar a PyPI:
    python setup.py sdist upload -r pypi
"""

import shutil
import os

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()
shutil.copy("README.md", os.path.join("docs", "README.md"))

with open('HISTORY.md') as history_file:
    history = history_file.read()

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]

test_requirements = [
    "nose",
    "coverage",
    "mock"
]

long_description = readme + '\n\n' + history
setup(
    name='data_cleaner',
    version='0.2.0',
    description="Paquete para limpieza de datos, segun estandares del equipo de Datos Argentina",
    long_description_content_type='text/markdown',
    long_description="",
    author="Datos Argentina",
    author_email='datos@modernizacion.gob.ar',
    url='https://github.com/datosgobar/data-cleaner',
    packages=[
        'data_cleaner'
    ],
    package_dir={
        'data_cleaner': 'data_cleaner'
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='data-cleaner',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
