#!/usr/bin/env python

from setuptools import setup

exec(open("pst/info.py").read())

setup(
    name="pst",
    version=__version__,
    author="mixed.connections",
    author_email="mixed.connections2@gmail.com",
    description="A light-weight version of pstree",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    url="https://github.com/mixedconnections/pst",
    packages=["pst"],
    scripts=["bin/pst"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Utilities",
    ],
    keywords = "shell pstree",
    license = "MIT"
)
