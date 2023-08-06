import re

from setuptools import find_packages, setup

version = re.search('^__version__\s*=\s*"(.*)"', open("cognite/turbulent_flux/__init__.py").read(), re.M).group(1)

setup(
    name="cognite-turbulent-flux-sdk",
    version=version,
    packages=["cognite." + p for p in find_packages(where="cognite")],
    install_requires=['pandas', 'numpy', 'scipy', 'requests'],
    python_requires=">=3.5",
)
