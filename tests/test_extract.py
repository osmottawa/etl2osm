# -*- coding: utf-8 -*-
import etl2osm
import pytest
from test_variables import roads, crs


def test_extract_topojson():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['topojson'])


def test_extract_kml():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['kml'])


def test_extract_osm():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['osm'])


def test_extract_unknown():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['unknown'])


def test_extract_zero():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['geojson-zero'])


def test_extract_file_extension():
    with pytest.raises(ValueError):
        etl2osm.extract("/path-not-exist.topojson")

    with pytest.raises(ValueError):
        etl2osm.extract("/path-not-exist.shp")


def test_extract_blank():
    with pytest.raises(ValueError):
        etl2osm.extract(roads['geojson-blank'])


def test_extract_lookup():
    data = etl2osm.extract(roads['geojson'])
    assert data[0]


def test_extract_add():
    data1 = etl2osm.extract(roads['geojson'])
    data2 = etl2osm.extract(roads['geojson'])
    assert len(data1) == 3
    assert len(data2) == 3
    assert len(data1 + data2) == 6


def test_extract_geojson():
    data = etl2osm.extract(roads['geojson'])
    assert data.crs == crs
    assert data.epsg == 'EPSG:4326'
    assert data.geojson
    assert data.geometry == 'LineString'
    assert data.properties
    assert len(data)


def test_extract_geojson_crs():
    data = etl2osm.extract(roads['geojson-WGS84'])
    assert data.geometry == 'LineString'
    assert data.properties
    assert data.crs == crs
    assert data.epsg == 'EPSG:4326'


def test_extract_shapefile():
    data = etl2osm.extract(roads['shp'])
    assert data.wkt
    assert data.epsg == 'EPSG:4326'
    assert data.crs
    assert data.geojson
    assert len(data)


def test_extract_lake_county_roads():
    data = etl2osm.extract(roads['lake_county'])
    assert data.geojson
    assert len(data)


if __name__ == '__main__':
    test_extract_shapefile()
    test_extract_geojson()
    test_extract_kml()
