import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="planefigures",
    version="0.3.0",
    author="Othniel Dona Monote",
    author_email="othnieldona@gmail.com",
    description="A turtle based package that makes drawing common geometric plane shapes a breeze.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/OthnielDona/planefigures",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)