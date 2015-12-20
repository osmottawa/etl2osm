# -*- coding: utf-8 -*-
import os
from test_variables import config, roads
import subprocess

infile = roads['lake_county']
outfile = 'tmp-file.geojson'
config = config['lake_county']['roads']


def test_cli_process():
    subprocess.call(['etl2osm', infile, '--config', config, '--outfile', outfile])
    assert os.path.exists(outfile)
    os.remove(outfile)

    subprocess.call(['etl2osm', infile, '--outfile', outfile])
    assert os.path.exists(outfile)
    os.remove(outfile)


if __name__ == '__main__':
    test_cli_process()
