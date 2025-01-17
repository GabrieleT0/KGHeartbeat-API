# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="kgheartbeat",
    version="0.2.6",
    description="Library that allows to perform Knowledge Graph (Linked Open Data) quality analysis.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://gabrielet0.github.io/KGHeartbeat-API/reference/",
    author="Gabriele Tuozzo, Maria Angela Pellegrino",
    author_email="gabrieletuozzo@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["kgheartbeat"],
    include_package_data=True,
    install_requires=["SPARQLWrapper>=2.0.0","networkx>=2.6.3","validators>=0.18.2","requests>=2.27.1","rdflib>=6.1.1","numpy>=1.19.5","mmh3>=3.0.0","mechanize>=0.4.7","bitarray>=2.4.0","scipy>=1.7.3"],
    package_data={'' : ['*.txt','*.gpickle']},
)