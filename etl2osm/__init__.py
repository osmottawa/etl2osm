# -*- coding: utf-8 -*-

from __future__ import absolute_import

__title__ = 'etl2osm'
__author__ = 'OSM Canada Team'
__author_email__ = 'carriere.denis@gmail.com'
__version__ = '0.0.1'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2015 OSM Canada Team'

# CLI
from etl2osm.cli import cli  # noqa
from etl2osm.api import process, extract, transform, load  # noqa
from etl2osm.transform import reproject  # noqa
