#!/usr/bin/env python3
import os.path
from setuptools import setup, find_packages


with open("README.rst") as f:
    long_description = f.read()

setup(
    name="dunder_run",
    version='0.1.0',
    author="Agustin Scaramuzza",
    author_email="agustinscaramuzza@gmail.com",
    license="GPLv3",
    description="A proof-of-concept for a new way of running Python scripts.",
    long_description=long_description,
    keywords=[],
    packages=['dunder_run'],
    url="https://github.com/scaramagus/dunder-run",
    entry_points = {
        'console_scripts': ['dunder_run=dunder_run.__main__:main'],
    }
)
