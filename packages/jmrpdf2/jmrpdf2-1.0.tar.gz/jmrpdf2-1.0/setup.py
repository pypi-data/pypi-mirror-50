import setuptools
from pathlib import Path

setuptools.setup(
    name="jmrpdf2",
    version=1.0,
    long_description="demo for Pypi",
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
