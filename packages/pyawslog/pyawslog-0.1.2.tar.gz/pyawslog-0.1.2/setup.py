import os.path

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyawslog",
    version="0.1.2",
    author="Maurya Allimuthu",
    author_email="catchmaurya@gmail.com",
    description="Python AWS Custom Log",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catchmaurya/pyawslog",
    packages=find_packages(),
    scripts=['pyawslog.py'],
    install_requires=['boto3>=1.9'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
