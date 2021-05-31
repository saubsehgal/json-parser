from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="json_parser",
    version="0.0.1",
    description="Json To Python Class Object Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms='any',
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pysimdjson"],
    extras_require={
        'test': [
            'pytest',
            'flake8',
            'coverage',
            'pytest-benchmark'
        ]
    }
)
