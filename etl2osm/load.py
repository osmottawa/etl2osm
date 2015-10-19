# -*- coding: utf-8 -*-

from __future__ import absolute_import
import fiona
from fiona.crs import from_epsg
from etl2osm.transform import reproject, transform_columns, read_config


class Load(object):
    def __init__(self, data, outfile, config=''):
        config = read_config(config)
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

if __name__ == "__main__":
    pass
