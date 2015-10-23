# -*- coding: utf-8 -*-

from codecs import open
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('etl2osm/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

requires = ['click', 'six']

setup(
    name='etl2osm',
    version=version,
    description="Extract, Transform and Load to OpenStreetMap.",
    long_description=readme,
    author='OSM Canada Team',
    author_email='carriere.denis@gmail.com',
    url='https://github.com/osmottawa/etl2osm/',
    download_url='https://github.com/osmottawa/etl2osm/',
    license="The MIT License",
    entry_points='''
        [console_scripts]
        etl2osm=etl2osm.cli:cli
    ''',
    packages=['etl2osm'],
    package_data={'': ['LICENSE', 'README.rst']},
    package_dir={'etl2osm': 'etl2osm'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    keywords='etl extract transform load shapefile geojson osm',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
