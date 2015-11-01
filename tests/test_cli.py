# -*- coding: utf-8 -*-
import os
from test_variables import config, roads
import subprocess


def test_cli_process():
    infile = roads['lake_county']
    outfile = 'tmp-file.geojson'
    lake_county = config['lake_county']['roads']

    # Execute Process Command
    subprocess.call(['etl2osm', infile, '--config', lake_county, '--outfile', outfile])
    assert os.path.exists(outfile)
    os.remove(outfile)


if __name__ == '__main__':
    test_cli_process()
