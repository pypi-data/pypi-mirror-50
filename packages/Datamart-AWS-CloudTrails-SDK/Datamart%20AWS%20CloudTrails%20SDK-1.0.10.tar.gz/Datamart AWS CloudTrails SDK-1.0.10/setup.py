import os

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


VERSION = os.environ.get("TAG_VERSION")
VERSION = VERSION[1:] if VERSION else "0.0.25"

setuptools.setup(
    name="Datamart AWS CloudTrails SDK",
    version=VERSION,
    author="Yaisel Hurtado, Raydel Miranda, Yordano Gonzalez",
    author_email="hurta2yaisel@gmail.com, raydel.miranda.gomez@gmail.com, yorda891216@gmail.com",
    description="AWS Python CloudTrails SDK for Logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/elasbit/dm-cloudtrails-sdk-py",
    packages=setuptools.find_packages(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <3.8",
    classifiers=(
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent"
    ),
)
