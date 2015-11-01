# -*- coding: utf-8 -*-
import os
import etl2osm
import pytest
from test_variables import config, roads, addresses


def test_load_kml():
    outfile = 'tmp-file.kml'
    data = etl2osm.extract(roads['geojson'])
    with pytest.raises(ValueError):
        data.save(outfile)


def test_load_osm():
    outfile = 'tmp-file.osm'
    data = etl2osm.extract(roads['geojson'])
    data.save(outfile)
    assert os.path.exists(outfile)
    os.remove(outfile)

    data = etl2osm.extract(addresses['geojson'])
    data.save(outfile)
    assert os.path.exists(outfile)
    os.remove(outfile)


def test_load_geojson():
    outfile = 'tmp-file.geojson'
    data = etl2osm.extract(roads['lake_county'])
    data.transform(config['lake_county']['roads'])
    data.save(outfile)
    assert os.path.exists(outfile)
    os.remove(outfile)


def test_load_shapefile():
    outfile = 'tmp-file.shp'
    basename = os.path.splitext(outfile)[0]

    data = etl2osm.extract(roads['lake_county'])
    data.transform(config['lake_county']['roads'])
    data.save(outfile)

    for ext in ['.shp', '.cpg', '.dbf', '.prj', '.shx']:
        filepath = ''.join((basename, ext))
        assert os.path.exists(filepath)
        os.remove(filepath)

if __name__ == '__main__':
    # test_load_geojson()
    test_load_osm()
    test_load_kml()
