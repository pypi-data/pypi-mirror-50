import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sbio",
    version="0.0.2",
    author="Tod Stuber",
    author_email="tod.p.stuber@usda.gov",
    description="Collection of simple bioinformatic tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/USDA-VS/sbio",
    packages=setuptools.find_packages(),
    install_requires=['python>=3.6', 're', 'pandas', 'numpy', 'concurrent', 'collections', 'gzip', 'argparse', 'textwrap', 'humanize'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

import os
import re
import pandas as pd
import numpy as np
pd.set_option("display.max_colwidth", 800) #prevents truncated reads
from concurrent import futures
from collections import namedtuple 
import gzip
import argparse
import textwrap
import humanize