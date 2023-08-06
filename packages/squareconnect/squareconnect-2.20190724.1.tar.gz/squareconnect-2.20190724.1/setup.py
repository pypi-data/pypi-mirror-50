# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "squareconnect"
VERSION = "2.20190724.1"

if sys.version_info[0] < 3:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
else:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Square Connect v2 Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "Square Inc.",
    author_email="",
    url="https://github.com/square/connect-python-sdk",
    keywords=["Swagger", "Square Connect API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    license="http://www.apache.org/licenses/LICENSE-2.0",
    include_package_data=True
)


