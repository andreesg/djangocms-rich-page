# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REQUIREMENTS = [
    'django-taggit<0.12',
    'django-filer',
    'django_select2',
    'djangocms-text-ckeditor',
    'django-appconf',
    'django-classy-tags',
    'south>=0.8',
    'django-hvad',
    'aldryn_gallery',
    'unidecode',
]

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='djangocms-rich-page',
    version='0.1',
    description='Adds content to django CMS 3 pages.',
    author='André Gonçalves',
    author_email='andre@goncalves.me',
    url='https://github.com/andreesg/djangocms-rich-page',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    keywords='djangocms-rich-page'
)
