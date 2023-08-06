import re
from os import path

from setuptools import find_packages, setup

version = re.search('^__version__\s*=\s*"(.*)"', open("cognite/turbulent_flux/__init__.py").read(), re.M).group(1)


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cognite-turbulent-flux-sdk",
    version=version,
    packages=["cognite." + p for p in find_packages(where="cognite")],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas', 'numpy', 'scipy', 'requests'],
    python_requires=">=3.7",
)
