from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pattmatch',
    version='0.0.0',
    description='Implementation of pattern matching algorithms',
    long_description=long_description,
    url='https://github.com/monzita/pattmatch',
    author='Monika Ilieva',
    author_email='hidden@hidden.com',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 3.6'
    ],
    license='GNU General Public License v3 or later (GPLv3+)',
    keywords='pattern-matching text string pattern python3',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'venv']),
)