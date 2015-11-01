# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
import etl2osm


@click.command()
@click.argument('infile')
@click.option('--config', '-c', help='Config file for column transformation.')
@click.option('--outfile', '-o', help='Out file path to save.')
def cli(infile, config, outfile):
    """Command Line Interface for ETL2OSM"""

    etl2osm.process(infile, config, outfile)
