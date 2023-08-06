import io
import os
import re

from setuptools import find_packages
from setuptools import setup

from envrun import __version__


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="envrun-python",
    version=__version__,
    url="https://github.com/ericgj/envrun-python",
    license="MIT",
    author="Eric Gjertsen",
    author_email="ericgj72@gmail.com",
    description="Run command with specified environment-variable file",
    long_description=read("README.rst"),
    packages=find_packages(exclude=("test",)),
    install_requires=["ruamel.yaml"],
    entry_points={"console_scripts": ["envrun = envrun.__main__:main"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
