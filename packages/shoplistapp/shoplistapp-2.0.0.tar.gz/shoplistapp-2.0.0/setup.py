#!/usr/bin/env python
import os
import sys
from setuptools import find_packages, setup
from os import path
from io import open

here = path.abspath(path.dirname(__file__))


VERSION = "2.0.0"
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

"""class VerifyVersionCommand(install):
    Custom command to verify that the git tag matches our version
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(tag, VERSION)
            sys.exit(info)"""
setup(
    name='shoplistapp',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='A simple Django app to keep a record of shopping list items.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.app.com/',
    author='Johnson Kaberere',
    author_email='kaguithiajohnson@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',],
    scripts=['manage.py'],

)
