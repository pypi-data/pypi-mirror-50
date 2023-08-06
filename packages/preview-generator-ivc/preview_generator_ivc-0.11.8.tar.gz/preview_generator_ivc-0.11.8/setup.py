# -*- coding: utf-8 -*-
# python setup.py sdist upload -r pypi


import os
import sys
from typing import List

from preview_generator import infos

py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    documentation = open(os.path.join(here, "README.rst")).read()
except IOError:
    documentation = ""
except UnicodeDecodeError:
    documentation = ""

testpkgs = []  # type: List[str]

tests_require = ["pytest"]

devtools_require = ["flake8", "isort", "mypy", "pre-commit"]

# add black for python 3.6+
if sys.version_info.major == 3 and sys.version_info.minor >= 6:
    devtools_require.append("black")

setup(
    name="preview_generator_ivc",
    version=infos.__version__,
    description=(
        "A library for generating preview (thumbnails, text or json overview) "
        "for file-based content"
    ),
    long_description=documentation,
    author="Algoo",
    author_email="contact@algoo.fr",
    url="https://github.com/ivc-inform/preview-generator.git",
    download_url=(
        "https://github.com/algoo/preview-generator/archive/release_{}.tar.gz".format(
            infos.__version__
        )
    ),
    keywords=["preview", "preview_generator", "thumbnail", "cache"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["ez_setup"]),
    python_requires=">= 3.6",
    include_package_data=True,
    extras_require={"testing": tests_require, "dev": tests_require + devtools_require},
    test_suite="py.test",  # TODO : change test_suite
    tests_require=testpkgs,
    package_data={"preview_generator": ["i18n/*/LC_MESSAGES/*.mo", "templates/*/*", "public/*/*"]},
    entry_points={"console_scripts": ["preview = preview_generator.__main__:main"]},
)
