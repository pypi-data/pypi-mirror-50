try:
    from setuptools import setup,  find_packages
except ImportError:
    from distutils.core import setup, find_packages

import loaders

setup(
    name='pyloaders',
    version=loaders.__version__,
    description='Basic animated ASCII loaders for Python scripts',
    license="GPL",
    long_description=open("README.md", 'r').read(),
    long_description_content_type="text/markdown",
    author='Matthew Levy',
    author_email='matt@webkolektiv.com',
    url="https://gitlab.com/ml394/pyloaders.git",
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
