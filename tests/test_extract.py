# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import etl2osm
import os
import pytest


root = os.path.dirname(etl2osm.__file__)[:-len('etl2osm')]
roads = {
    'shp': os.path.join(root, "tests/shapefile/roads.shp"),
    'geojson': os.path.join(root, "tests/geojson/roads.geojson"),
    'topojson': os.path.join(root, "tests/topojson/roads.topojson"),
    'kml': os.path.join(root, "tests/kml/roads.kml")
}

wkt = 'GEOGCS["GCS_WGS_1984",DATUM["WGS_1984",SPHEROID["WGS_84",6378137,298.257223563]]'\
      ',PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],AUTHORITY["EPSG","4326"]]'
epsg = 'EPSG:4326'
crs = {'type': 'name', 'properties': {'name': 'EPSG:4326'}}


def test_extract_topojson():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['topojson'])


def test_extract_kml():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['kml'])


def test_extract_file_extension():
    with pytest.raises(ValueError):
        etl2osm.extract("/path-not-exist.topojson")

    with pytest.raises(ValueError):
        etl2osm.extract("/path-not-exist.shp")


def test_extract_add():
    data1 = etl2osm.extract(roads['geojson'])
    data2 = etl2osm.extract(roads['geojson'])
    assert len(data1) == 3
    assert len(data2) == 3
    assert len(data1 + data2) == 6


def test_extract_geojson():
    data = etl2osm.extract(roads['geojson'])
    assert data.crs == crs
    assert len(data)


def test_extract_geojson_transform():
    data = etl2osm.extract(roads['geojson'])
    data.transform()
    assert len(data)


def test_extract_shapefile():
    data = etl2osm.extract(roads['shp'])
    assert data.wkt == wkt
    assert data.epsg == epsg
    assert data.crs == crs
    assert len(data)


def test_extract_shapefile_transform():
    data = etl2osm.extract(roads['shp'])
    data.transform()
    assert len(data)


if __name__ == '__main__':
    # test_extract_shapefile()
    # test_extract_geojson()
    test_extract_kml()
