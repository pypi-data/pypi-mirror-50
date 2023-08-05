# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="jwt_client_authentication",
    version="0.1.2.beta",
    description="Pip package for authenticating a JWT token with a remote jwt backend",
    license="MIT",
    author="kobededecker",
    packages=find_packages(),
    install_requires=["pyjwt"],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
