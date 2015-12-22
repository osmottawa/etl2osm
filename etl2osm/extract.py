# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import os
import fiona
import json
from etl2osm.transform import (reproject,
                               transform_columns,
                               extract_epsg,
                               config_to_properties,
                               confirm_geometry,
                               get_coordinate_rerefence_system)
from etl2osm.load import Load
from osgeo import osr


class Extract(Load):
    def __init__(self, infile, **kwargs):
        # Reset Values
        self.features = []
        self.wkt = None
        self.epsg = None

        if isinstance(infile, dict):
            self.read_geojson(infile)
        else:
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
        """Reads a Shapefile and gives the results in GeoJSON format
        Speed = 0.35ms/feature
        """

        logging.info('Reading Shapefile: %s' % infile)

        with fiona.drivers():
            with fiona.open(infile) as source:
                self.geometry = set([source.meta['schema']['geometry']])
                self.properties = source.meta['schema']['properties']

                # Read EPSG
                crs = source.meta['crs']

                if 'init' in crs:
                    self.epsg = crs['init'].upper()
                elif 'crs_wkt' in source.meta:
                    self.wkt = source.meta['crs_wkt']
                else:
                    logging.warning('Coordinate Reference System was not detected (default=EPSG:4326)')
                    self.epsg = 'EPSG:4326'

                for feature in source:
                    if feature:
                        if feature['geometry']:
                            feature = confirm_geometry(feature)
                            self.features.append(feature)
                        else:
                            logging.warning('Could not find [geometry] in feature.')

    def read_geojson(self, infile, **kwargs):
        """Reads a GeoJSON and gives the results in GeoJSON format
        Speed = 0.091ms/feature"""

        logging.info('Reading GeoJSON: %s' % infile)
        if isinstance(infile, dict):
            geojson = infile
        else:
            with open(infile) as f:
                geojson = json.load(f)

        if 'type' not in geojson:
            raise ValueError('GeoJSON must contain a [type] "FeatureCollection" or "Feature"')
        if 'crs' not in geojson:
            logging.warning('Coordinate Reference System was not detected (default=EPSG:4326)')
            self.epsg = 'EPSG:4326'
        else:
            self.epsg = 'EPSG:{}'.format(extract_epsg(geojson['crs']))

        # Read GeoJSON Feature Collection
        if geojson['type'] == 'FeatureCollection':
            if not geojson['features']:
                raise ValueError('FeatureCollection has [0] features.')
            features = geojson['features']

        # Read Single GeoJSON Feature
        elif geojson['type'] == 'Feature':
            features = [geojson]

        properties = set()
        self.geometry = set()

        for feature in features:
            # Add unique attribute keys to properties
            if 'properties' in feature:
                properties.update(feature['properties'].keys())

            # Only add features with geometry
            if feature.get('geometry'):
                feature = confirm_geometry(feature)
                self.features.append(feature)
                self.geometry.update([feature['geometry']['type']])
            else:
                logging.warning('Could not find [geometry] in feature.')

        # Creating basic properties for attribute table when building a shapefile.
        self.properties = dict((key, 'str') for key in properties)

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

    def transform(self, config='', **kwargs):
        """ Transform the data using the config file """

        if 'crs_target' in kwargs:
            crs_target = kwargs.pop('crs_target', 'EPSG:4326')
            self.epsg = crs_target
        else:
            crs_target = 'EPSG:4326'
            self.epsg = 'EPSG:4326'
            self.wkt = osr.SRS_WKT_WGS84

        crs_target = get_coordinate_rerefence_system(extract_epsg(crs_target))
        crs_source = get_coordinate_rerefence_system(extract_epsg(self.crs))

        if config:
            self.properties = config_to_properties(config)

        for x, feature in enumerate(self.features):
            # Detect if correct geometry (Multipoints > Point)
            feature = confirm_geometry(feature)

            # Reproject data to target projection (crs_target=4326)
            if kwargs.get('reproject', True):
                reproject(feature, crs_source, crs_target)

            # Transform Columns
            if config:
                feature = transform_columns(feature, config, **kwargs)

            # Save feature to self
            self[x] = feature


if __name__ == '__main__':
    pass
