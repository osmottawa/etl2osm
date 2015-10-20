# -*- coding: utf-8 -*-

from __future__ import absolute_import
import re
import os
import click
import logging
from etl2osm.api import process


@click.command()
@click.argument('infiles', nargs=-1)
@click.option('--output', '-o', help='Output file path to save.')
@click.option('--config', '-c', help='Config file for column transformation.')
@click.option('--format', '-f', default='osm', help='Data output format [shp, geojson, osm].')
@click.option('--debug', is_flag=True, help='Shows all the logging messages.')
def cli(infiles, debug, **kwargs):
    """Command Line Interface for ETL2OSM"""

    # Enable Debugging
    if "debug" in kwargs: #Check if debug exists
        if kwargs['debug']:
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # Process Input files
    if infiles:
        # Using the search all function
        # Ex: ais kml/2015*.kml (Will find all files starting with 2015 and end with .kml)
        if '*' in infiles[0]:
            start, end = re.split('\*', infiles[0])
            root, start = os.path.split(start)

            # When user is using the * function inside a folder
            if not root:
                root = '.'

            # Show all files within the end folder directory
            for infile in os.listdir(root):

                # Find Matching with the begining & end in between the *
                pattern = r'^{0}.+{1}$'.format(start, end)
                match = re.search(pattern, infile)

                # Process the files found
                if match:
                    infile = os.path.join(root, infile)
                    process(infile, **kwargs)
        else:
            # Hard coded files as a list
            for infile in infiles:
                process(infile, **kwargs)

    # No input files provided
    else:
        click.echo('Please include an input file path:\n'
                   'etl2osm filepath/example.shp')

if __name__ == '__main__':
    cli()
