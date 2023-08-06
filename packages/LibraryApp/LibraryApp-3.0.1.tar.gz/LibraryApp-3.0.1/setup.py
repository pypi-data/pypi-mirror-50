import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='LibraryApp',
    version='3.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple django library app ',
    long_description=README,
    author='kevin',
    author_email='kevin@kev.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

    ],
    install_requires=[
        # Should only have the most basic
        'Django>=1.11.22,<=2.2.2',
        'djangorestframework==3.9.4',
        'celery>=3.1.16'
        'psycopg2>=2.8.3'
        'psycopg2-binary>=2.8.3'
    ],
    scripts=[
        "bin/locallibrary_app"
    ],
)

#u7VSC2gjqNXPtms