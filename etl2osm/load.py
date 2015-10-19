# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import logging
import fiona
from fiona.crs import from_epsg
from etl2osm.transform import reproject, transform_columns, read_config


class Load(object):
    def __init__(self, data, outfile, **kwargs):
        extension = os.path.splitext(outfile)[1][1:]
        config = read_config(kwargs['config'])

        write_file = {
            'osm': self.write_osm,
            'geojson': self.write_geojson,
            'shp': self.write_shp,
            'kml': self.write_kml,
        }
        write_file[extension](data, outfile, config, **kwargs)

    def write_shapefile(self, data, outfile, config, **kwargs):
        """ Writes data to Shapefile format """

        properties = dict((key, 'str') for key in config['conform'].keys())
        # Default Coordinate reference system is WGS84
        crs = from_epsg(4326)
        driver = 'ESRI Shapefile'
        encoding = 'utf-8'
        schema = data.schema
        schema['properties'] = properties

        with fiona.open(outfile, 'w', driver=driver, schema=schema, crs=crs, encoding=encoding) as sink:
            for feature in data:
                # Reproject data to WGS84 before saving
                feature = reproject(feature, data.crs_wkt, 4326)
                feature = transform_columns(feature, config)
                sink.write(feature)

    def write_osm(self, data, outfile, config, **kwargs):
        """ Writes data to OSM format """

        logging.info('Writing OSM: %s' % outfile)
        return ValueError('Writing OSM not implemented')

    def write_kml(self, data, outfile, config, **kwargs):
        """ Writes data to KML format """

        logging.info('Writing KML: %s' % outfile)
        return ValueError('Writing KML not implemented')

    def write_geojson(self, data, outfile, config, **kwargs):
        """ Writes data to GeoJSON format """

        logging.info('Writing GeoJSON: %s' % outfile)
        return ValueError('Writing GeoJSON not implemented')


if __name__ == "__main__":
    pass
