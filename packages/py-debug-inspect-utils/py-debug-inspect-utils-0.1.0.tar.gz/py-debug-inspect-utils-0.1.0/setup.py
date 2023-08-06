#!/usr/bin/env python

from os.path import isfile

from setuptools import setup


def _read_file(path):
    with open(path) as fp:
        return fp.read().strip()


if isfile("README.md"):
    long_description = _read_file("README.md")
else:
    long_description = ""

setup(
    name="py-debug-inspect-utils",
    author="NyanKiyoshi",
    author_email="hello@vanille.bid",
    url="https://github.com/NyanKiyoshi/py-debug-inspect-utils/",
    description="Utils to inspect a stack to quickly debug 'magic' libraries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.0",
    packages=["py_debug_inspect_utils"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: Public Domain",
    ],
    zip_safe=False,
)
