import os
from setuptools import find_packages, setup

def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "profiles",
    packages = find_packages(),
    include_package_data=True,
    version = "0.1",
    description = "Generic extensible django user profiles.",
    author = "Incuna Ltd",
    author_email = "admin@incuna.com",
    url = "http://incuna.com/",
    long_description=fread("README"),
)
