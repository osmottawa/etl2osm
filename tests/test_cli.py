# -*- coding: utf-8 -*-
import os
from test_variables import roads
import subprocess

infile = roads['geojson']
outfile = 'tmp-file.geojson'
config = '{"foo": {"text": "bar"}}'


def test_cli_process():
    subprocess.call(['etl2osm', infile, '--config', config, '--outfile', outfile])
    assert os.path.exists(outfile)
    os.remove(outfile)

    subprocess.call(['etl2osm', infile, '--outfile', outfile])
    assert os.path.exists(outfile)
    os.remove(outfile)


if __name__ == '__main__':
    test_cli_process()
