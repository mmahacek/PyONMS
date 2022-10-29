import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="PyONMS",
    version="0.0.3",
    author="Mark Mahacek",
    author_email="mmahacek@opennms.com",
    packages=["pyonms", "pyonms.dao", "pyonms.models", "pyonms.portal", "pyonms.utils"],
    url="https://github.com/mmahacek/PyONMS",
    license="LICENSE.txt",
    description="A Python library for accessing the OpenNMS REST API.",
    long_description=read("README.md"),
    install_requires=["requests", "python-dotenv", "xmltodict", "tqdm"],
)
