# -*- coding: utf-8 -*-

import etl2osm


def test_entry_points():
    etl2osm.process
    etl2osm.extract
    etl2osm.transform
    etl2osm.load


def test_transform_projection_epsg_4326():
    feature = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [100.0, 0.5]}
    }
    assert etl2osm.reproject(feature, 4326, 4326) == feature
