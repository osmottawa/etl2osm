# -*- coding: utf-8 -*-
import os
import etl2osm
import pytest
from collections import OrderedDict
from test_variables import wkt, epsg, crs, roads, config


root = os.path.dirname(etl2osm.__file__)[:-len('etl2osm')]


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
    config = {
        "conform": {
            "address": "ADDRESS",
            "number": "NUMBER",
        }
    }
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
    feature = etl2osm.transform_columns(feature, config)
    assert feature == result


def test_transform_columns_dict():
    config = {
        "conform": {
            "number": {'field': "NUMBER", 'int': True}
        }
    }
    feature = {
        "type": "Feature",
        "properties": {
            "NUMBER": "65"
        }
    }
    result = {
        "type": "Feature",
        "properties": OrderedDict(
            number=65
        )
    }
    feature = etl2osm.transform_columns(feature, config)
    assert feature == result


def test_transform_columns_list():
    config = {
        "conform": {
            "street": ["NUMBER", "STREET"]
        }
    }
    feature = {
        "type": "Feature",
        "properties": {
            "NUMBER": "65",
            "STREET": "Rideau Street"
        }
    }
    result = {
        "type": "Feature",
        "properties": OrderedDict(
            street="65 Rideau Street"
        )
    }
    feature = etl2osm.transform_columns(feature, config)
    assert feature == result


def test_transform_clean_regex():
    conform = {'function': 'regexp', 'field': 'NAME', 'pattern': '^([0-9]+)'}
    properties = {'NAME': '65 Street Name'}
    assert etl2osm.clean_field(properties, conform) == '65'


def test_transform_clean_regex_replace():
    conform = {'function': 'regexp', 'field': 'NAME', 'pattern': '^(HWY)', 'replace': 'Highway'}
    properties = {'NAME': 'HWY 174'}
    assert etl2osm.clean_field(properties, conform) == 'Highway 174'


def test_transform_clean_regex_int():
    conform = {'function': 'regexp', 'field': 'NAME', 'pattern': '^([0-9]+)', 'int': True}
    properties = {'NAME': '65 Street Name'}
    assert etl2osm.clean_field(properties, conform) == 65


def test_transform_clean_int():
    conform = {'field': 'NUMBER', 'int': True}
    properties = {'NUMBER': '65'}
    assert etl2osm.clean_field(properties, conform) == 65


def test_transform_clean_float():
    conform = {'field': 'NUMBER', 'float': True}
    properties = {'NUMBER': '65.145'}
    assert etl2osm.clean_field(properties, conform) == 65.145


def test_transform_clean_join():
    conform = {'function': 'join', 'fields': ["NUMBER", "STREET"], 'separator': ' - '}
    properties = {'NUMBER': '65', 'STREET': "Rideau Street"}
    assert etl2osm.clean_field(properties, conform) == '65 - Rideau Street'


def test_transform_clean_suffix():
    conform = {'function': 'suffix', 'field': "STREET"}
    properties = {'STREET': "AVE"}
    path = os.path.join(root, 'tests', 'models', 'suffix.json')
    assert etl2osm.clean_field(properties, conform) == 'Avenue'
    assert etl2osm.clean_field(properties, conform, suffix={'AVE': 'Avenue'}) == 'Avenue'
    assert etl2osm.clean_field(properties, conform, suffix=path) == 'Avenue'


def test_transform_clean_direction():
    conform = {'function': 'direction', 'field': "DIRECTION"}
    properties = {'DIRECTION': "NE"}
    path = os.path.join(root, 'tests', 'models', 'direction.json')
    assert etl2osm.clean_field(properties, conform) == 'Northeast'
    assert etl2osm.clean_field(properties, conform, direction={'NE': 'Northeast'}) == 'Northeast'
    assert etl2osm.clean_field(properties, conform, direction=path) == 'Northeast'


def test_transform_clean_title():
    conform = {'function': 'title', 'field': "NAME"}
    properties = {'NAME': "3RD AVENUE"}
    path = os.path.join(root, 'tests', 'models', 'title_except.json')
    assert etl2osm.clean_field(properties, conform) == '3rd Avenue'
    assert etl2osm.clean_field(properties, conform, title_except=['rd']) == '3rd Avenue'
    assert etl2osm.clean_field(properties, conform, title_except=path) == '3rd Avenue'

    properties = {'NAME': None}
    assert not etl2osm.clean_field(properties, conform)

    properties = {'NAME': 2}
    assert etl2osm.clean_field(properties, conform) == 2
    assert etl2osm.clean_field(properties, conform, title_except=['rd']) == 2
    assert etl2osm.clean_field(properties, conform, title_except=path) == 2


def test_transform_clean_mph():
    conform = {'function': 'mph', 'field': "SPEED"}
    properties = {'SPEED': "55"}
    assert etl2osm.clean_field(properties, conform) == '55 mph'


def test_transform_clean_text():
    conform = {'text': 'Lake County'}
    properties = {'NO': "CLUE"}
    assert etl2osm.clean_field(properties, conform) == 'Lake County'


def test_transform_geojson():
    data = etl2osm.extract(roads['lake_county'])
    data.transform()
    assert data.epsg == 'EPSG:4326'


def test_transform_geojson_config():
    data = etl2osm.extract(roads['lake_county'])
    data.transform()
    assert data[0]['properties']['FullStreet'] == u'LENZE DR'
    assert data[0]['properties']['NumberOfLa'] == u'2'

    data.transform(config['lake_county']['roads'])
    assert data[0]['properties']['street'] == 'Lenze Drive'
    assert data[0]['properties']['lanes'] == 2
    assert data.epsg == 'EPSG:4326'


def test_transform_config_to_properties():
    properties = etl2osm.config_to_properties(config['numbers'])
    assert properties
    assert properties['str'] == 'str'
    assert properties['int'] == 'int'
    assert properties['float'] == 'float'

    with pytest.raises(ValueError):
        etl2osm.config_to_properties(config['no-conform'])


if __name__ == '__main__':
    # test_transform_columns_basic()
    # test_transform_regex()
    # test_transform_regex_replace()
    # test_transform_regex_int()
    # test_transform_int()
    # test_transform_float()
    # test_transform_geojson_config()
    test_transform_geojson_config()
    test_reproject_polygon_holes()