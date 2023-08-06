import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = "-n auto"

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


NAME = "filingsdb"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23",
]

setup(
    name=NAME,
    version=VERSION,
    description="filingsdb api library",
    author="FilingsDB",
    author_email="info@filingsdb.com",
    url="https://filingsdb.com",
    license="MIT",
    keywords=["filingsdb", "sec", "library", "filings", "data", "api"],
    install_requires=REQUIRES,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    tests_require=[
        "pytest >= 4.6.2, < 4.7",
        "pytest-mock >= 1.10.4",
        "pytest-xdist >= 1.28.0",
        "pytest-cov >= 2.7.1",
        # coverage 5.0 pre-releases don't work, and setuptools doesn't ignore
        # pre-releases (cf. https://github.com/pypa/setuptools/issues/855)
        "coverage >= 4.5.3, < 5",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    cmdclass={"test": PyTest},
    zip_safe=False,
    long_description="""\
    The Filingsdb API client library in python.
    """,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
