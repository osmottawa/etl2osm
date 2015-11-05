# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
import etl2osm


@click.command()
@click.argument('infile')
@click.option('--config', '-c', help='Config file for column transformation.')
@click.option('--outfile', '-o', help='Out file path to save.')
@click.option('--suffix', help='Filepath for suffix attribute function.')
@click.option('--direction', help='Filepath for direction attribute function.')
@click.option('--title_except', help='Filepath for title except attribute function.')
def cli(infile, config, outfile, **kwargs):
    """Command Line Interface for ETL2OSM"""

    etl2osm.process(infile, config, outfile, **kwargs)
