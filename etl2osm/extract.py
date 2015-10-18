# -*- coding: utf-8 -*-

from __future__ import absolute_import
import logging
import os
import fiona


class Extract(object):
    def __init__(self, infile, **kwargs):
        # Reset Values
        self.geojson = []
        self.crs = ''
        self.crs_wkt = ''
        self.extension = os.path.splitext(infile)[1][1:]

        read_file = {
            'osm': self.read_osm,
            'geojson': self.read_geojson,
            'shp': self.read_shp,
            'kml': self.read_kml,
        }

        # Error detection
        if not os.path.exists(infile):
            raise ValueError('File path does not exist: %s' % infile)

        if self.extension not in read_file:
            raise ValueError('etl2osm cannot read file extension: %s' % self.extension)

        read_file[self.extension](infile, **kwargs)

    def __len__(self):
        return len(self.geojson)

    def __iter__(self):
        for feature in self.geojson:
            yield feature

    def __add__(self, data):
        for feature in data:
            self.geojson.append(feature)
        return self

    def __repr__(self):
        return '<Data [%i]>' % len(self)

    def __getitem__(self, lookup):
        return self.geojson[lookup]

    def read_shp(self, infile, **kwargs):
        """Reads a Shapefile and gives the results in GeoJSON format"""

        logging.info('Reading Shapefile: %s' % infile)

        with fiona.drivers():
            with fiona.open(infile) as source:
                self.meta = source.meta
                self.schema = source.meta['schema']
                self.crs = source.meta['crs']
                self.crs_wkt = source.meta['crs_wkt']
                for feature in source:
                    self.geojson.append(feature)

    def read_kml(self, infile, **kwargs):
        """Reads a KML and gives the results in GeoJSON format"""

        logging.info('Reading KML: %s' % infile)
        return ValueError('Reading KML not implemented')

    def read_geojson(self, infile, **kwargs):
        """Reads a GeoJSON and gives the results in GeoJSON format"""

        logging.info('Reading GeoJSON: %s' % infile)
        return ValueError('Reading GeoJSON not implemented')

    def read_osm(self, infile, **kwargs):
        """Reads a OSM and gives the results in GeoJSON format"""

        logging.info('Reading OSM: %s' % infile)
        return ValueError('Reading OSM not implemented')

    def transform(self):
        pass

    def load(self):
        pass

    def save(self):
        pass


if __name__ == '__main__':
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    infile = 'C:\Users\Claude\Downloads/Address2015.shp'
    data = Extract(infile)
    print(data)
