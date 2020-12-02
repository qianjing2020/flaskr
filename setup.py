# setup.py

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    url="https://github.com/qianjing/flaskr",
    # automatically find package directories and python files
    packages=find_packages(),
    # include_package_data is to include other files, such as the static and templates directories, see manifest for the package data included.
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
