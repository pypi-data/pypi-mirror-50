from setuptools import find_packages, setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='lazyeda',
    packages=find_packages(),
    version='0.1.4',
    description='Lazy EDA is a python library to help shorten the coding time for basic understanding  of data, EDA techniques and repetitive tasks with less lines of code',
    author='Shankar Rao Pandala',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
)
