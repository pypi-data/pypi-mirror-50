import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setuptools.setup(
    name="diagonal",
    version="0.0.2",
    author="opxyc",
    #author_email="xxxxxxxxxxxxx@gmail.com",
    description="A small collection of functions to get various diagonals of a 2d matrix",
    #url="https://github.com/pypa/example-project",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    long_description=long_description,
    long_description_content_type='text/markdown'
)