import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-jo-blog-app',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='blog app to nenable users to share posts',
    long_description=README,
    url='https://www.example.com/',
    author='Your Name',
    author_email='john.maluki12@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    install_requires=[
        'Django>=2.1.0,<=2.2.2',
        'djangorestframework==3.9.4',
        'celery>=3.1.16'
    ],
)
