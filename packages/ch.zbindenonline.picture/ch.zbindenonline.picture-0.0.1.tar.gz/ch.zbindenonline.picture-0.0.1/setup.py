# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="ch.zbindenonline.picture",
    version="0.0.1",
    description="A library to handle pictures",
    license="MIT",
    author="Patrick Zbinden",
    packages=find_packages(),
    install_requires=['Pillow', 'click'],
    entry_points={
        'console_scripts':[
        'crop=ch.zbindenonline.picture.crop:crop'
        ]
    },
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
