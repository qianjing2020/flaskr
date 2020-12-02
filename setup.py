# setup.py

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    url="https://github.com/qianjing2020/flaskr",
    description="Flask - flaskr tutorial",
    long_description="This is a web application for user to register, login, logout their account. Upon login, users can create, edit, delete or save their blogs. Source codes were adopted from Flask official tutorial to create web app flaskr.",
    # automatically find package directories and python files
    packages=find_packages(),
    # include_package_data is to include other files, such as the static and templates directories, see manifest for the package data included.
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
