import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

with open(os.path.join(here, "sesamutils", 'VERSION.txt')) as f:
    VERSION = f.read().strip()

setup(
    name='sesamutils',
    version=VERSION,
    description='Sesam microservice utils',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Anders Borud',
    url='https://github.com/sesam-community/',
    packages=find_packages()
)
