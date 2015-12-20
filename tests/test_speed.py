# -*- coding: utf-8 -*-
from datetime import datetime
from test_variables import roads
import etl2osm


def test_speed_extract_geojson(infile=roads['geojson']):
    """
    GeoJSON: 50 ms/feature
    """
    before = datetime.now()
    data = etl2osm.extract(infile)
    microseconds = (datetime.now() - before).microseconds
    print 'count: {} | time: {} ms/feature'.format(len(data), microseconds / len(data))


def test_speed_extract_shapefile(infile=roads['shp']):
    """
    Shapefile: 250~500 ms/feature
    """
    before = datetime.now()
    data = etl2osm.extract(infile)
    microseconds = (datetime.now() - before).microseconds
    print 'count: {} | time: {} ms/feature'.format(len(data), microseconds / len(data))


def test_speed_transform_false(infile=roads['geojson']):
    """
    Geometry: set(['LineString']) | Reproject: False | count: 18809 | time: 1 ms/feature
    Geometry: set(['Point']) | Reproject: False | count: 31478 | time: 1 ms/feature
    Geometry: set(['Polygon']) | Reproject: False | count: 106218 | time: 1 ms/feature
    """
    data = etl2osm.extract(infile)
    before = datetime.now()
    data.transform(reproject=False)
    microseconds = (datetime.now() - before).microseconds
    print 'Geometry: {} | Reproject: False | count: {} | time: {} ms/feature'.format(
        data.geometry,
        len(data),
        microseconds / len(data)
    )


def test_speed_transform_true(infile=roads['geojson']):
    """
    Geometry: set(['Point']) | Reproject: True | count: 31478 | time: 10 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 18809 | time: 26 ms/feature
    Geometry: set(['Polygon']) | Reproject: True | count: 106218 | time: 3 ms/feature
    """
    data = etl2osm.extract(infile)
    before = datetime.now()
    data.transform(reproject=True)
    microseconds = (datetime.now() - before).microseconds
    print 'Geometry: {} | Reproject: True | count: {} | time: {} ms/feature'.format(
        data.geometry,
        len(data),
        microseconds / len(data)
    )


if __name__ == '__main__':
    infile = '/home/denis/Downloads/canvec_021G_shp/fo_1080019_2.shp'
    for i in range(5):
        test_speed_transform_true(infile=infile)
