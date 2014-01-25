#!/usr/bin/env python

"""google plus login integration for django.contrib.auth

A library that can be used to add google plus login support to Django applications.
The library integrates with Django's built in authentication system
"""

from distutils.core import setup


description, long_description = __doc__.split('\n\n', 1)
VERSION = '0.1'

setup(
    name='django-google-plus',
    version=VERSION,
    author='Venkatesh',
    description=description,
    long_description=long_description,
    author_email = "vbachu@iserviceglobe.com",
    url='https://github.com/venkatesh22/django_google_plus',
    download_url=('https://github.com/venkatesh22/django_google_plus/archive/master.zip'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    packages=[
        'django_google_plus',
        ],
    package_data={
        'django_google_plus': ['templates/google_plus/*.html'],
        },
    provides=['django_google_plus'],
    )
