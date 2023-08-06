import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="date-time-pkg",
    version="0.0.4",
    author="Mitch Ainslie",
    author_email="mitch.ainslie.it@gmail.com",
    description="Contains a date and time generator",
    long_description="Generates a file that contains different information",
    long_description_content_type="text/markdown",
    url="https://github.com/mitchainslieg/listdir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data = {
        '': ['*.ini']
    }
)