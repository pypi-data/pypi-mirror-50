#!/usr/bin/env python
from setuptools import find_namespace_packages, setup
from Cython.Build import cythonize
import numpy

setup(
    name="becke",
    version='0.0.1',
    description='Fast and memory efficient implimentation of becke weights.',
    auther='Derrick Yang',
    author_email='yxt1991@gmail.com',
    url='https://github.com/tczorro/becke.git',
    package_dir={"": "src"},
    ext_modules=cythonize("src/becke/*.pyx"),
    include_dirs=[numpy.get_include()],
    packages=find_namespace_packages(where="src"),
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy>=1.16", "cython>=0.29"]
)
