from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="perfmon",
    version="0.0.3",
    author="tiantain",
    author_email="858898530@qq.com",
    description="A Python library for test android perf .",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/roberchen820/forgetme",
    packages=['perfmon'],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=True,
)