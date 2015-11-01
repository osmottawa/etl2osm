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


if __name__ == '__main__':
    test_load_geojson()
