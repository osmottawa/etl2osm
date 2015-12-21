# -*- coding: utf-8 -*-
import os
import etl2osm
from collections import OrderedDict
from test_variables import wkt, epsg, crs, roads


root = os.path.dirname(etl2osm.__file__)[:-len('etl2osm')]
models = etl2osm.Models()


def test_reproject_point():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [100.0, 0.5]
        }
    }
    assert etl2osm.reproject(feature, epsg, epsg) == feature
    assert etl2osm.reproject(feature, wkt, epsg) == feature
    assert etl2osm.reproject(feature, wkt, wkt) == feature
    assert etl2osm.reproject(feature, epsg, wkt) == feature
    assert etl2osm.reproject(feature, crs, epsg) == feature
    assert etl2osm.reproject(feature, crs, wkt) == feature
    assert etl2osm.reproject(feature, crs, crs) == feature


def test_reproject_linestring():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [[100.0, 0.0], [101.0, 1.0]]
        }
    }
    assert etl2osm.reproject(feature, epsg, epsg) == feature
    assert etl2osm.reproject(feature, wkt, epsg) == feature
    assert etl2osm.reproject(feature, wkt, wkt) == feature
    assert etl2osm.reproject(feature, epsg, wkt) == feature


def test_reproject_polygon():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]
            ]
        }
    }
    assert etl2osm.reproject(feature, epsg, epsg) == feature
    assert etl2osm.reproject(feature, wkt, epsg) == feature
    assert etl2osm.reproject(feature, wkt, wkt) == feature
    assert etl2osm.reproject(feature, epsg, wkt) == feature


def test_reproject_polygon_holes():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]
            ]
        }
    }
    assert etl2osm.reproject(feature, epsg, epsg) == feature
    assert etl2osm.reproject(feature, wkt, epsg) == feature
    assert etl2osm.reproject(feature, wkt, wkt) == feature
    assert etl2osm.reproject(feature, epsg, wkt) == feature


def test_reproject_multi_linestring():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [
                [[100.0, 0.0], [101.0, 1.0]],
                [[102.0, 2.0], [103.0, 3.0]]
            ]
        }
    }
    assert etl2osm.reproject(feature, epsg, epsg) == feature
    assert etl2osm.reproject(feature, wkt, epsg) == feature
    assert etl2osm.reproject(feature, wkt, wkt) == feature
    assert etl2osm.reproject(feature, epsg, wkt) == feature


def test_reproject_multi_point():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "MultiPoint",
            "coordinates": [[100.0, 0.0], [101.0, 1.0]]
        }
    }
    assert etl2osm.reproject(feature, epsg, epsg) == feature
    assert etl2osm.reproject(feature, wkt, epsg) == feature
    assert etl2osm.reproject(feature, wkt, wkt) == feature
    assert etl2osm.reproject(feature, epsg, wkt) == feature


def test_reproject_geometry_collection():
    # Not implemented
    # http://geojson.org/geojson-spec.html#geometrycollection
    pass


def test_transform_columns_string():
    conform = {"address": "ADDRESS", "number": "NUMBER"}
    feature = {
        "type": "Feature",
        "properties": {
            "ADDRESS": "Highway 41",
            "NUMBER": "65"
        }
    }
    result = {
        "type": "Feature",
        "properties": OrderedDict(
            address="Highway 41",
            number="65"
        )
    }
    feature = etl2osm.transform_columns(feature, conform)
    assert feature == result


def test_transform_clean_suffix():
    conform = {'model': 'suffix', 'field': "STREET"}
    properties = {'STREET': "AVE"}
    model = etl2osm.Models()
    model['suffix'] = {'AVE': 'Avenue'}
    assert etl2osm.clean_field(properties, conform) == 'Avenue'
    assert etl2osm.clean_field(properties, conform, model={'AVE': 'Avenue'}) == 'Avenue'
    assert etl2osm.clean_field(properties, conform, model=model) == 'Avenue'


def test_transform_clean_direction():
    conform = {'model': 'direction', 'field': "DIRECTION"}
    properties = {'DIRECTION': "NE"}
    model = etl2osm.Models()
    model['direction'] = {'NE': 'Northeast'}
    assert etl2osm.clean_field(properties, conform) == 'Northeast'
    assert etl2osm.clean_field(properties, conform, model={'NE': 'Northeast'}) == 'Northeast'
    assert etl2osm.clean_field(properties, conform, model=model) == 'Northeast'


def test_transform_clean_title():
    conform = {'title': True, 'field': "NAME"}
    properties = {'NAME': "3RD AVENUE"}
    assert etl2osm.clean_field(properties, conform) == '3rd Avenue'
    assert etl2osm.clean_field(properties, conform) == '3rd Avenue'

    properties = {'NAME': None}
    assert not etl2osm.clean_field(properties, conform)

    properties = {'NAME': 2}
    assert etl2osm.clean_field(properties, conform) == 2
    assert etl2osm.clean_field(properties, conform) == 2
    assert etl2osm.clean_field(properties, conform) == 2


def test_transform_clean_text():
    conform = {'text': 'Lake County'}
    properties = {'NO': "CLUE"}
    assert etl2osm.clean_field(properties, conform) == 'Lake County'


def test_transform_geojson():
    data = etl2osm.extract(roads['lake_county'])
    data.transform()
    assert data.epsg == 'EPSG:4326'


def test_transform_confirm_geometry():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "MultiPoint",
            "coordinates": [[100.0, 0.0]]
        }
    }
    print etl2osm.confirm_geometry(feature)

if __name__ == '__main__':
    # test_transform_columns_basic()
    # test_transform_regex()
    # test_transform_regex_replace()
    # test_transform_regex_int()
    # test_transform_int()
    # test_transform_float()
    # test_transform_geojson_config()
    test_transform_clean_suffix()
