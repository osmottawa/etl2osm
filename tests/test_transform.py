# -*- encoding: utf-8 -*-

import etl2osm


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
