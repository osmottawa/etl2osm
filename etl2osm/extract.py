# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
import logging
import os
import fiona
import json
from etl2osm.transform import reproject, transform_columns, read_config, extract_epsg
from osgeo import osr


class Extract(object):
    def __init__(self, infile, **kwargs):
        # Reset Values
        self.features = []
        self.wkt = ''
        self.epsg = ''
        extension = os.path.splitext(infile)[1][1:]

        read_file = {
            'osm': self.read_osm,
            'geojson': self.read_geojson,
            'json': self.read_geojson,
            'shp': self.read_shp,
            'kml': self.read_kml,
            'topojson': self.read_topojson
        }

        # Error detection
        if not os.path.exists(infile):
            raise ValueError('File path does not exist: %s' % infile)

        if extension not in read_file:
            raise ValueError('etl2osm cannot read file extension: %s' % extension)

        read_file[extension](infile, **kwargs)

    def __len__(self):
        return len(self.features)

    def __iter__(self):
        for feature in self.features:
            yield feature

    def __add__(self, data):
        for feature in data:
            self.features.append(feature)
        return self

    def __repr__(self):
        return '<Data [%i]>' % len(self)

    def __setitem__(self, key, value):
        self.features[key] = value
        return value

    def __getitem__(self, key):
        return self.features[key]

    @property
    def crs(self):
        if self.epsg:
            return {"type": "name", "properties": {"name": self.epsg}}

        elif self.wkt:
            return {"type": "name", "properties": {"name": self.wkt}}

    @property
    def geojson(self):
        return {"type": "FeatureCollection", "crs": self.crs, "features": self.features}

    def read_shp(self, infile, **kwargs):
        """Reads a Shapefile and gives the results in GeoJSON format"""

        logging.info('Reading Shapefile: %s' % infile)

        with fiona.drivers():
            with fiona.open(infile) as source:
                self.meta = source.meta
                self.schema = source.meta['schema']
                self.wkt = source.meta['crs_wkt']

                # Read EPSG
                crs = source.meta['crs']
                if 'init' in crs:
                    self.epsg = crs['init'].upper()

                for feature in source:
                    self.features.append(feature)

    def read_geojson(self, infile, **kwargs):
        """Reads a GeoJSON and gives the results in GeoJSON format"""

        logging.info('Reading GeoJSON: %s' % infile)

        with open(infile) as f:
            geojson = json.load(f)

            if 'type' not in geojson:
                raise ValueError('GeoJSON must contain a [type] "FeatureCollection" or "Feature"')
            if 'crs' not in geojson:
                logging.warning('Coordinate Reference System was not detected (default=EPSG:4326)')
                self.epsg = 'EPSG:4326'
            else:
                self.epsg = 'EPSG:{0}'.format(extract_epsg(geojson['crs']))

            # Read Feature Collection
            if geojson['type'] == 'FeatureCollection':
                for feature in geojson['features']:
                    self.features.append(feature)

    def read_topojson(self, infile, **kwargs):
        """Reads a TopoJSON and gives the results in GeoJSON format"""

        logging.info('Reading TopoJSON: %s' % infile)
        raise ValueError('Reading TopoJSON not implemented')

    def read_kml(self, infile, **kwargs):
        """Reads a KML and gives the results in GeoJSON format"""

        logging.info('Reading KML: %s' % infile)
        raise ValueError('Reading KML not implemented')

    def read_osm(self, infile, **kwargs):
        """Reads a OSM and gives the results in GeoJSON format"""

        logging.info('Reading OSM: %s' % infile)
        raise ValueError('Reading OSM not implemented')

    def transform(self, config={}):
        """ Transform the data using the config file """

        config = read_config(config)

        for x, feature in enumerate(self.features):
            # Reproject data to WGS84
            if not self.epsg == 'ESPG:4326':
                feature = reproject(feature, self.crs, osr.SRS_WKT_WGS84)

            # Transform Columns
            if config:
                feature = transform_columns(feature, config)

            # Save feature to self
            self[x] = feature

        self.epsg = 'EPSG:4326'
        self.wkt = osr.SRS_WKT_WGS84


if __name__ == '__main__':
    pass
