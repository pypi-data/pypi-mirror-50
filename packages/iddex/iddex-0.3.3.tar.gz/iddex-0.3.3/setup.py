#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

try:
    codecs.lookup("mbcs")
except LookupError:
    ascii = codecs.lookup("ascii")
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == "mbcs"))

VERSION = "0.3.3"
URL = "https://gitlab.com/id.dex-pub/python-iddex"

setup(
    name="iddex",
    version=VERSION,
    description="Python library for iddex",
    long_description=open("README.md").read(),
    download_url="{}/tarball/{}".format(URL, VERSION),
    author="Fabian Schuh",
    author_email="Fabian@chainsquad.com",
    maintainer="Fabian Schuh",
    maintainer_email="Fabian@chainsquad.com",
    url=URL,
    keywords=["iddex", "library", "api", "rpc"],
    packages=["iddex", "iddexapi", "iddexbase"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
