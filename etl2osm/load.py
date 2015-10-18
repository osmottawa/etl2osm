# -*- coding: utf-8 -*-

from __future__ import absolute_import
import fiona
from fiona.crs import from_epsg
from etl2osm import reproject


class Load(object):
    def __init__(self, data, outfile, **kwargs):
        # Default Coordinate reference system is WGS84
        self.save(data, outfile)

    def save(self, data, outfile):
        crs = from_epsg(4326)
        driver = 'ESRI Shapefile'
        encoding = 'utf-8'
        schema = data.schema

        with fiona.open(outfile, 'w', driver=driver, schema=schema, crs=crs, encoding=encoding) as sink:
            for feature in data:
                # Reproject data to WGS84 before saving
                feature = reproject(feature, data.crs_wkt, 4326)
                sink.write(feature)

if __name__ == "__main__":
    from extract import Extract

    infile = 'C:\Users\Claude\Downloads/Address2015.shp'
    outfile = 'C:\Users\Claude\Downloads/AddressTEST.shp'
    data = Extract(infile)
    Load(data, outfile)
