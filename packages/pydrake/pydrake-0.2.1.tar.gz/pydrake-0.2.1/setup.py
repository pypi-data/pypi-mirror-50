"""
   Copyright 2019 Jacob Padley

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst")) as readme:
    long_desc = readme.read()

setup(
    name="pydrake",
    version="0.2.1",
    description="Experimental Python API Wrapper for the Riot Games API.",
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    url="https://github.com/JPadley18/pydrake",
    author="Jacob Padley",
    author_email="jacob5180@hotmail.co.uk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="riot league legends wrapper api pydrake drake",
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=[
        'certifi',
        'chardet',
        'idna',
        'requests',
        'urllib3'
    ],
    download_url="https://github.com/JPadley18/pydrake/archive/v0.2.1.tar.gz"
)
