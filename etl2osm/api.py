#!/usr/bin/python
# coding: utf8


import os
import re
import json
import logging
import fiona
from collections import OrderedDict
from bs4 import BeautifulSoup


def clean_data(value):
    """Cleans data before going into dataset"""

    # Format extra space in middle for integers
    # Example: 123 456 >> 123456
    pattern = r'(\d+)\s(\d+)'
    match = re.search(pattern, value)
    if match:
        return int(''.join(match.groups()))

    # Try to convert to Int
    try:
        return int(value)
    except:
        pass

    # Try to convert to Float
    try:
        return float(value)

    # Returns value as a String
    except:
        return value.strip()


def process(infile, **kwargs):
    """Reads the KML document and saves it into a GeoJSON document"""

    # Optional Parameters
    outfile = kwargs.get('out')
    format = kwargs.get('format')

    # Read KML
    logging.info('Reading AIS KML: %s' % infile)
    geojson = read_kml(infile)

    # Uses the same file path as the input file but replaces the file extension for GeoJSON/Shapefile
    if not outfile:
        outfile = '.'.join((os.path.splitext(infile)[0], format))
    else:
        outfile = '.'.join((os.path.splitext(outfile)[0], format))

    # Save GeoJSON
    if format == 'geojson':
        logging.info('Saving GeoJSON: %s' % outfile)
        write_geojson(geojson, outfile)

    # Save Shapefile
    if format == 'shp':
        logging.info('Saving Shapefile: %s' % outfile)
        write_shapefile(geojson, outfile)


def write_shapefile(geojson, outfile):
    """Creates a Shapefile document"""

    # Fiona must have data types as strings
    lookup = {
        str: 'str',
        int: 'int',
        float: 'float',
        unicode: 'str'
    }

    # Fiona schema for attribute table
    properties = OrderedDict((k, lookup[type(v)]) for k, v in geojson['features'][0]['properties'].items())

    # Shapefile parameters
    crs = {'init': 'epsg:4326'}
    driver = 'ESRI Shapefile'
    encoding = 'utf-8'
    schema = {
        'geometry': '3D LineString',
        'properties': properties
    }

    # Create Shapefile
    with fiona.open(outfile, 'w', driver=driver, schema=schema, crs=crs, encoding=encoding) as sink:
        for feature in geojson['features']:
            sink.write(feature)


def write_geojson(geojson, outfile):
    """Creates a GeoJSON document"""

    with open(outfile, 'w') as f:
        f.write(json.dumps(geojson, indent=4))


def read_kml(infile):
    """Reads a KML and gives the results in GeoJSON format"""

    pass

if __name__ == '__main__':
    infile = 'C:\Users\carriere.d\Documents\GitHub\AIS\kml\\20130801000000_20130831235959_ClassAPosition_Tracks.kml'
    process(infile, format='shp')
