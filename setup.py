from os.path import dirname, join
from setuptools import find_packages, setup

from profiles import get_version

def fread(fname):
    return open(join(dirname(__file__), fname)).read()

setup(
    name = "django-profiles",
    packages = find_packages(),
    include_package_data=True,
    version = get_version(),
    description = "Generic extensible django user profiles.",
    author = "Incuna Ltd",
    author_email = "admin@incuna.com",
    url = "http://incuna.com/",
    long_description=fread("README"),
)

