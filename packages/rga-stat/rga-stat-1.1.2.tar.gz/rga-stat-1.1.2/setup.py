#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:15:34 2019

@author: arpitaggarwal
"""

from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="rga-stat",
    version="1.1.2",
    description="A Python package to get statistical functions.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/arpit12011995/rga-stat",
    author="rga packages ",
    author_email="rgapackages@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["rga_stat"],
    include_package_data=True,
    install_requires=["pandas", "numpy"],
)
