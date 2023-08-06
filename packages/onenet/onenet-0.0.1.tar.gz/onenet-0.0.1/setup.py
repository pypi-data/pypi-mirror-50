#!/usr/bin/env python3
# encoding: utf-8
import sys, os, re
from setuptools import setup
import onenet

repo_url = "https://github.com/menduo/onenet-python-sdk"
packages = ["onenet"]
keywords = ["onenet" ] + ['onenet', 'chinamobile', 'iot']

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

about = {}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'onenet', '__version__.py'), 'r') as f:
    exec(f.read(), about)


setup(
    name = "onenet",
    version=about["__version__"],
    keywords=keywords,
    description="China Mobile OneNet Python SDK",
    long_description="see more at:\n%s\n" % repo_url,
    license="MIT",
    url=repo_url,
    author="menduo",
    author_email="shimenduo@gmail.com",
    packages=packages,
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[],
)
