# -*- encoding: utf-8 -*-

import etl2osm
from collections import OrderedDict


def test_reproject_point():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [100.0, 0.5]
        }
    }
    assert etl2osm.reproject(feature, 4326) == feature


def test_reproject_linestring():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [[100.0, 0.0], [101.0, 1.0]]
        }
    }
    assert etl2osm.reproject(feature, 4326) == feature


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
    assert etl2osm.reproject(feature, 4326) == feature


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
    assert etl2osm.reproject(feature, 4326) == feature


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
    assert etl2osm.reproject(feature, 4326) == feature


def test_reproject_multi_point():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "MultiPoint",
            "coordinates": [[100.0, 0.0], [101.0, 1.0]]
        }
    }
    assert etl2osm.reproject(feature, 4326) == feature


def test_reproject_geometry_collection():
    # Not implemented
    # http://geojson.org/geojson-spec.html#geometrycollection
    pass


def test_transform_columns_basic():
    config = {
        "conform": {
            "address": "ADDR",
            "full": "FULL",
        }
    }
    feature = {
        "type": "Feature",
        "properties": {
            "ADDR": "HWY 41",
            "FULL": "65 Street Name"
        }
    }
    result = {
        "type": "Feature",
        "properties": OrderedDict(
            address="HWY 41",
            full="65 Street Name"
        )
    }

    feature = etl2osm.transform_columns(feature, config)
    assert feature == result
