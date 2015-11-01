# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import etl2osm
from test_variables import config, roads


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
    test_load_shapefile()
