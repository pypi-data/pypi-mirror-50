#!/usr/bin/env python3
from setuptools import setup


setup(
    name='django-testuser',
    version='0.6.0',
    author='Victor',
    author_email='victor@what.digital',
    url='https://gitlab.com/what-digital/django-testuser',
    packages=[
        'test_user',
    ],
    include_package_data=True,
    install_requires=[
        'django >= 2.1',
        'django-env-settings >= 0.12.0',
    ],
)
