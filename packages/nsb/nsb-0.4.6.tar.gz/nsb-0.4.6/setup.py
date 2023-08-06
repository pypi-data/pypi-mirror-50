from setuptools import setup
import nsb.__about__ as about

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'nsb',
    packages = ['nsb', 'nsb/gaia', 'nsb/mypycat'],
    version = about.__version__,
    description = about.__description__,
    long_description = long_description,
    long_description_content_type='text/markdown',
    author= about.__author__,
    author_email= about.__author_email__,
    url='https://pypi.python.org/pypi/nsb',
    install_requires=['healpy','tqdm', 'ephem', 'astropy', 'scipy', 'numpy', 'matplotlib'],
    package_dir={'nsb': 'nsb'},
    package_data={'nsb': ['gaia/ducaticat.txt']},
    entry_points = {
        "console_scripts": ['nsb = nsb.__main__:main']
        },
    classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Operating System :: POSIX :: Linux',
              'Topic :: Scientific/Engineering :: Astronomy',
              'Topic :: Scientific/Engineering :: Atmospheric Science',
              'Topic :: Scientific/Engineering :: Physics',
              ],
)

import http.client
import urllib.parse
import time
from xml.dom.minidom import parseString
