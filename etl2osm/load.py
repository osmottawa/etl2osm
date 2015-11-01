# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
import os
import json
import logging
import fiona
from fiona.crs import from_epsg


class Load(object):
    def save(self, outfile):
        """ Saves file to path """

        extension = os.path.splitext(outfile)[1][1:]
        write_file = {
            'osm': self.write_osm,
            'geojson': self.write_geojson,
            'shp': self.write_shapefile,
            'kml': self.write_kml,
        }
        write_file[extension](outfile)

    def write_shapefile(self, outfile):
        """ Writes data to Shapefile format """

        # Default Coordinate reference system is WGS84
        crs = from_epsg(4326)
        driver = 'ESRI Shapefile'
        encoding = 'utf-8'
        schema = {
            'geometry': self.geometry,
            'properties': self.properties
        }

        with fiona.open(outfile, 'w', driver=driver, schema=schema, crs=crs, encoding=encoding) as sink:
            for feature in self.features:
                sink.write(feature)

    def write_osm(self, outfile):
        """ Writes data to OSM format """

        logging.info('Writing OSM: %s' % outfile)
        raise ValueError('Writing OSM not implemented')

    def write_kml(self, outfile):
        """ Writes data to KML format """

        logging.info('Writing KML: %s' % outfile)
        raise ValueError('Writing KML not implemented')

    def write_geojson(self, outfile):
        """ Writes data to GeoJSON format """

        logging.info('Writing GeoJSON: %s' % outfile)

        with open(outfile, 'wb') as f:
            f.write(json.dumps(self.geojson, indent=4))
