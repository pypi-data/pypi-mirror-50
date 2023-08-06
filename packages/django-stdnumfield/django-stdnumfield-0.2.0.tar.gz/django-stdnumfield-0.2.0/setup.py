# coding=utf-8
import os
from setuptools import setup

import stdnumfield

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("README.md", 'r') as f:
    description = f.read()

setup(
    name="django-stdnumfield",
    version=stdnumfield.VERSION,
    packages=["stdnumfield"],
    install_requires=["python-stdnum>=1.11,<1.12"],
    extras_require={
        "dev": [
            "prettyprinter",
            "Django>=2.2",
            "coverage",
            "flake8",
            "tox",
            "mock",
            "black",
            "twine",
        ],
        "ci": [
            "Django>=2.2",
            "coverage",
            "flake8",
            "tox",
            "mock",
            "black",
        ],
    },
    include_package_data=True,
    license="The Unlicense",
    description=(
        "Simple Django form and model fields for working with stdnum fields."),
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/frnhr/django-stdnumfield",
    author="Fran Hrzenjak",
    author_email="fran@changeset.hr",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: Freeware",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
