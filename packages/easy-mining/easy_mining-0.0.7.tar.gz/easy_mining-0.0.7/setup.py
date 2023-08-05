# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_mining",
    version="0.0.7",
    author="Noluye",
    author_email="1183851628@qq.com",
    description="an easy way of data mining.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Noluye/easy_mining",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
