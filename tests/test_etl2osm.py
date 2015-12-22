# -*- coding: utf-8 -*-
import os
import etl2osm
from test_variables import roads


def test_entry_points():
    etl2osm.process
    etl2osm.extract
    etl2osm.transform
    etl2osm.load
    etl2osm.reproject


def test_api_process():
    outfile = 'tmp-filepath.geojson'
    data = etl2osm.process(roads['geojson'], outfile, config={'foo': {'text': 'bar'}})
    assert data.geojson
    assert data.epsg
    assert os.path.exists(outfile)
    os.remove(outfile)

    data = etl2osm.process(roads['geojson'], outfile)
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
