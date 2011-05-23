import os
from distutils.core import setup

VERSION = '0.1'

classifiers = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Environment :: Web Environment",
    "Framework :: Django",
]

setup(
    name='django-adminsettings',
    version=VERSION,
    url='https://github.com/Threespot/django-adminsettings',
    author='Chuck Harmston',
    author_email='chuck.harmston@threespot.com',
    packages=['adminsettings'],
    package_dir={'adminsettings': 'adminsettings'},
    description=(
        'System for defining settings controllable by the user in Django\'s '
        'admin interface'
    ),
    classifiers=classifiers,
    install_requires=[
        'django>=1.3',
    ],
)