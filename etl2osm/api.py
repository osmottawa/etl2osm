# -*- coding: utf-8 -*-
from __future__ import absolute_import
from etl2osm.extract import Extract


def process(infile, config, outfile, **kwargs):
    """ All in one process for doing ETL2OSM

    :argument ``infile``: Input file path to read.
    :param ``outfile``: Output file path to save.
    :param ``config``: Config file for column transformation.
    :param ``format``: Data output format [shp, geojson, osm].
    """

    data = Extract(infile, **kwargs)
    data.transform(config, **kwargs)
    data.save(outfile, **kwargs)
    return data


def extract(infile, **kwargs):
    """ Extracts data from file path.

    :argument ``infile``: Input file path to read.
    """
    return Extract(infile, **kwargs)
