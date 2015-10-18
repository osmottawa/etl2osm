#!/usr/bin/python
# coding: utf8


import os
import re
import json
import logging
import fiona
from collections import OrderedDict


def process(infile, **kwargs):
    """Reads the KML document and saves it into a GeoJSON document"""

    # Enable Debugging
    if kwargs['debug']:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # Read config file
    config = kwargs['config']
    if config:
        if not os.path.exists(config):
            raise ValueError('Config file path does not exist: %s' % config)
        with open(config) as f:
            config = json.load(f)
    print(config)
    exit()

    # Get InFile file extension
    infile_ext = os.path.splitext(infile)[1][1:]
    
    # Get outfile file extension
    outfile = kwargs.get('outfile')
    if outfile:
        outfile_ext = os.path.splitext(outfile)[1][1:]
        outfile = '.'.join((os.path.splitext(outfile)[0], outfile_ext))
    else:
        # Uses the same file path as the input file but replaces the file extension
        # Defaults to OSM format if not outfile or format is defined
        outfile_ext = kwargs.get('format', 'osm')
        outfile = '.'.join((os.path.splitext(infile)[0], outfile_ext))

    # Reading File
    # ============
    read_file = {
        'osm': read_osm,
        'geojson': read_geojson,
        'shp': read_shp,
        'kml': read_kml,
    }
    if not os.path.exists(infile):
        raise ValueError('File path does not exist: %s' % infile)

    if not infile_ext in read_file:
        raise ValueError('etl2osm cannot read file extension: %s' % infile_ext)

    geojson = read_file[infile_ext](infile, **kwargs)

    # Saving File
    # ===========
    write_file = {
        'osm': write_osm,
        'geojson': write_geojson,
        'shp': write_shp,
        'kml': write_kml,
    }

    create_folder(outfile)


def create_folder(file_path):
    """Create folders if needed """

    if os.path.exists(os.path.split(file_path)[0]):
        return os.makedirs(os.path.split(file_path)[0])


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


def write_shapefile(geojson, outfile):
    """Creates a Shapefile document"""

    logging.info('Creating Shapefile: %s' % outfile)

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

    logging.info('Creating GeoJSON: %s' % outfile)

    with open(outfile, 'w') as f:
        f.write(json.dumps(geojson, indent=4))


def write_osm(geojson, outfile):
    """Creates a OSM document"""

    logging.info('Creating OSM: %s' % outfile)
    raise ValueError('Creating OSM not implemented')


def read_kml(infile, **kwargs):
    """Reads a KML and gives the results in GeoJSON format"""

    logging.info('Reading KML: %s' % infile)
    return ValueError('Reading KML not implemented')


def read_geojson(infile, **kwargs):
    """Reads a GeoJSON and gives the results in GeoJSON format"""

    logging.info('Reading GeoJSON: %s' % infile)
    return ValueError('Reading GeoJSON not implemented')

def read_osm(infile, **kwargs):
    """Reads a OSM and gives the results in GeoJSON format"""

    logging.info('Reading OSM: %s' % infile)
    return ValueError('Reading OSM not implemented')

def read_shp(infile, **kwargs):
    """Reads a Shapefile and gives the results in GeoJSON format"""

    logging.info('Reading Shapefile: %s' % infile)

if __name__ == '__main__':
    config = 'C:/Users/Claude/Documents/GitHub/TheVillages/sources/roads/lake_county.json'
    infile = 'C:\Users\Claude\Downloads\Roads (2)_201510150921267062\Roads.shp'
    process(infile, config=config, outfile='Roads.geojson', debug=True)
