# -*- coding: utf-8 -*-

from __future__ import absolute_import
from etl2osm.extract import Extract
from etl2osm.load import Load

def process(infile, **kwargs):
    """ All in one process for doing ETL2OSM

    :argument ``infile``: Input file path to read.
    :param ``outfile``: Output file path to save.
    :param ``config``: Config file for column transformation.
    :param ``format``: Data output format [shp, geojson, osm].
    """
    data = extract(infile,**kwargs)
    data = transform(data,**kwargs)
    load(data,infile=infile,outfile=kwargs["output"],**kwargs)
    raise ValueError('Process function is not implemented in the API yet.')
    pass


def extract(infile, **kwargs):
    """ Extracts data from file path.

    :argument ``infile``: Input file path to read.
    """
    return Extract(infile, **kwargs)



def transform(data, **kwargs):
    """ Transform data columns.

    :argument ``data``: Data that has already been extracted.
    :param ``config``: Config file for column transformation.
    """
    return data


def load(data,**kwargs):
    """ Loads data into a specific format.

    :argument ``data``: Data that has already been extracted.
    :param ``outfile``: Output file path to save.
    :param ``format``: Data output format [shp, geojson, osm].
    """
    Load(data, **kwargs)
