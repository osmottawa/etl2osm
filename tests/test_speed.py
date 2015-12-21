# -*- coding: utf-8 -*-
from datetime import datetime
from test_variables import roads
import etl2osm


def test_speed_extract_geojson(infile=roads['geojson']):
    """
    Geometry: set([u'LineString']) | count: 17057 | time: 36 ms/feature
    Geometry: set([u'LineString']) | count: 3 | time: 55 ms/feature
    """
    before = datetime.now()
    data = etl2osm.extract(infile)
    microseconds = (datetime.now() - before).microseconds
    print 'Geometry: {} | count: {} | time: {} ms/feature'.format(
        data.geometry,
        len(data),
        microseconds / len(data)
    )


def test_speed_extract_shapefile(infile=roads['shp']):
    """
    Geometry: set(['LineString']) | count: 3 | time: 302 ms/feature
    Geometry: set(['Polygon']) | count: 106218 | time: 1 ms/feature
    """
    before = datetime.now()
    data = etl2osm.extract(infile)
    microseconds = (datetime.now() - before).microseconds
    print 'Geometry: {} | count: {} | time: {} ms/feature'.format(
        data.geometry,
        len(data),
        microseconds / len(data)
    )


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
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 21 ms/feature
    Geometry: set(['Polygon']) | Reproject: True | count: 106218 | time: 3 ms/feature
    Geometry: set(['Polygon']) | Reproject: True | count: 106218 | time: 5 ms/feature
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
    """
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 8 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 28 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 26 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 17 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 32 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 27 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 31 ms/feature
    Geometry: set(['LineString']) | Reproject: True | count: 7015 | time: 30 ms/feature
    """
    infile = '/home/denis/Downloads/canvec_021G_shp/hd_1470009_1.shp'
    for i in range(5):
        test_speed_transform_true(infile)
