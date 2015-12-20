# -*- coding: utf-8 -*-
from datetime import datetime
from test_variables import config, roads
import etl2osm

infile = roads['geojson']
outfile = 'tmp-file.geojson'
config = config['lake_county']['roads']


def test_speed_extract():
    """
    4x GeoJSON = 0.091 ms/feature
    1x Shapefile = 0.35 ms/feature
    """
    before = datetime.now()
    extract = etl2osm.extract(infile)
    print 'count: {} | time: {} ms/feature'.format(len(extract), (datetime.now() - before) / len(extract) * 1000)


def test_speed_transform():
    """
    1x    With Reprojecting = 1.944 ms/feature
    2000x Without Reprojecting = 0.001 ms/feature
    """
    extract = etl2osm.extract(infile)
    before = datetime.now()
    print extract.epsg
    extract.transform(reproject=False)
    print 'count: {} | time: {} ms/feature'.format(len(extract), (datetime.now() - before) / len(extract) * 1000)

    before = datetime.now()
    extract.transform(reproject=True)
    print 'count: {} | time: {} ms/feature'.format(len(extract), (datetime.now() - before) / len(extract) * 1000)

if __name__ == '__main__':
    test_speed_transform()
