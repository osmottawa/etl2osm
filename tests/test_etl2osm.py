# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import etl2osm
from test_variables import config, roads


def test_entry_points():
    etl2osm.process
    etl2osm.extract
    etl2osm.transform
    etl2osm.load
    etl2osm.reproject


def test_api_process():
    outfile = 'tmp-filepath.geojson'
    data = etl2osm.process(roads['lake_county'], config['lake_county']['roads'], outfile)
    assert data.geojson
    assert data.epsg
    assert os.path.exists(outfile)
    os.remove(outfile)


def test_api_extract():
    data = etl2osm.extract(roads['geojson'])
    assert data.geojson
    assert data.epsg

if __name__ == '__main__':
    test_api_process()
    test_api_extract()
