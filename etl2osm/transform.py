# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import re
import json
import logging
from six import string_types, binary_type
from collections import OrderedDict
from osgeo import osr, ogr
from etl2osm.models import suffix, direction, cap_except


true_list = ['True', 'true', '1', True, 1]


def regex_strip(value):
    # ESRI Shapfiles have fields [SUB] blank fields at the end
    # Regex will search all characters but must END with a letter or number
    # Also acts as an .strip() function
    if isinstance(value, (string_types, binary_type)):
        match = re.search(r'^([a-z,A-Z,0-9].+[a-z,A-Z,0-9])', value)
        if match:
            value = match.group()
    return str(value)


def config_to_properties(config):
    properties = OrderedDict()
    config = read_config(config)

    if 'conform' not in config:
        raise ValueError('Config file missing [conform] to format attributes.')

    for key, value in config['conform'].items():
        datatype = 'str'

        # If value is a dictionary, looking for {'int': True}
        if isinstance(value, (dict)):
            if value.get('int') in true_list:
                datatype = 'int'
            elif value.get('float') in true_list:
                datatype = 'float'
        properties[key] = datatype

    return properties


def get_coordinate_rerefence_system(crs):
    projection = osr.SpatialReference()

    # Read Projection from EPSG or WKT
    # For all EPSG projections
    # http://spatialreference.org/ref/epsg/wgs-84/
    if isinstance(crs, int):
        valid = projection.ImportFromEPSG(crs)

    elif isinstance(crs, (string_types, binary_type)):
        valid = projection.ImportFromWkt(crs)
    else:
        raise ValueError('Cannot detect the type Coordinate Reference System (CRS)')

    # Check if results are valid (0 == Valid projection)
    if not valid == 0:
        raise ValueError('EPSG provided was invalid for CRS: {0}'.format(crs))

    logging.info('Get CRS: %s' % projection)
    return projection


def extract_epsg(crs):
    if isinstance(crs, (string_types, binary_type)):
        crs = crs.lower()
        if 'epsg:' in crs:
            return int(crs.replace('epsg:', ''))
    if isinstance(crs, dict):
        if crs['type'] == 'name':
            if 'properties' in crs:
                return extract_epsg(crs['properties']['name'])
            else:
                return extract_epsg(crs['name'])
    return crs


def reproject(feature, crs_source, crs_target=4326):
    # Source Projection
    p1 = get_coordinate_rerefence_system(extract_epsg(crs_source))

    # Output Projection (WGS84)
    p2 = get_coordinate_rerefence_system(extract_epsg(crs_target))

    geom = feature['geometry']
    coord = feature['geometry']['coordinates']

    convert = {
        'Point': convert_point,
        'LineString': convert_linestring,
        'Polygon': convert_polygon,
        'MultiLineString': convert_multi_linestring,
        'MultiPoint': convert_multi_point,
    }

    if geom['type'] not in convert:
        raise ValueError('Reproject geometry type not implemented: %s' % geom['type'])
    feature['geometry']['coordinates'] = convert[geom['type']](p1, p2, coord)

    return feature


def convert_point(p1, p2, coord):
    coord_trans = osr.CoordinateTransformation(p1, p2)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(coord[0], coord[1])
    point.Transform(coord_trans)

    return point.GetPoint_2D()


def convert_multi_point(p1, p2, coord):
    multi_point = []
    for point in coord:
        multi_point.append(convert_point(p1, p2, point))

    return multi_point


def convert_multi_linestring(p1, p2, coord):
    multi_line = []
    for line in coord:
        multi_line.append(convert_linestring(p1, p2, line))

    return multi_line


def convert_linestring(p1, p2, coord):
    line = []
    for point in coord:
        line.append(convert_point(p1, p2, point))

    return line


def convert_polygon(p1, p2, coord):
    polygon = []
    for line in coord:
        polygon.append(convert_linestring(p1, p2, line))

    return polygon


def read_config(config):
    if isinstance(config, dict):
        return config

    if not os.path.exists(config):
        raise ValueError('Config file path does not exist: %s' % config)

    with open(config) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def titlecase_except(value, exceptions=cap_except):
    if isinstance(value, (string_types, binary_type)):
        word_list = re.split(' ', value)
        final = []

        for word in word_list:
            if word in exceptions:
                final.append(word)
            else:
                final.append(word.capitalize())

        return ' '.join(final)
    return value


def clean_field(properties, conform):
    if 'field' in conform:
        # STRING
        if isinstance(conform, dict):
            field = conform['field']
            if field not in properties:
                raise ValueError('Cannot find attribute [%s] using the Attribute Function.' % field)
            value = properties[field]

    # DICT
    elif isinstance(conform, (string_types, binary_type)):
        field = conform
        if field not in properties:
            raise ValueError('Cannot find attribute [%s] using the Attribute Function.' % field)
        value = properties[field]

    # LIST
    elif isinstance(conform, (list, tuple)):
        values = []
        for field in conform:
            value = clean_field(properties, field)
            if value:
                values.append(value)
        value = ' '.join(values)

    # LIST using Fields
    elif 'fields' in conform:
        value = []
        for field in conform['fields']:
            if field not in properties:
                raise ValueError('Cannot find attribute [%s] using the Attribute Function.' % field)
            value.append(properties[field])

    # Attribute Functions
    if 'function' in conform:

        # Applies a Regex function match or replace from pattern.
        if 'regexp' in conform['function']:
            if 'field' not in conform:
                raise ValueError('[field] is missing using the Regex Attribute Function.')
            if 'pattern' not in conform:
                raise ValueError('[pattern] is missing using the Regex Attribute Function.')
            match = re.search(conform['pattern'], properties[field])
            value = match.group()
            if 'replace' in conform:
                value = properties[field].replace(value, conform['replace'])

        # Applies the Join attribute function
        elif 'join' in conform['function']:
            if 'fields' not in conform:
                raise ValueError('[fields] are missing using the Join Attribute Function.')
            if 'separator' not in conform:
                logging.warning('[separator] is missing using the Join Attribute Function.')
            separator = conform.get('separator', ' ')
            value = separator.join(value)

        # Replaces the abreviated suffix (AVE=Avenue)
        elif 'suffix' in conform['function']:
            if 'field' not in conform:
                raise ValueError('[field] is missing using the Suffix Attribute Function.')
            if properties[field]:
                if properties[field] not in suffix:
                    logging.warning('Suffix cannot be found [%s] in ETL2OSM models.' % properties[field])
                else:
                    value = suffix[str(properties[field])]

        # Replaces the abreviated directions (NE=Northeast)
        elif 'direction' in conform['function']:
            if 'field' not in conform:
                raise ValueError('[field] is missing using the Direction Attribute Function.')
            if properties[field]:
                if properties[field] not in direction:
                    logging.warning('Direction cannot be found [%s] in ETL2OSM models.' % properties[field])
                else:
                    value = direction[str(properties[field])]

        # Converts string to a nice Titlecase (3RD AVENUE=3rd Avenue)
        elif 'title' in conform['function']:
            if 'field' not in conform:
                raise ValueError('[field] is missing using the Title Attribute Function.')
            value = titlecase_except(properties[field])

        # Adds mph at the end of the integer field.
        elif 'mph' in conform['function']:
            if 'field' not in conform:
                raise ValueError('[field] is missing using the Mph Attribute Function.')
            value = '{0} mph'.format(properties[field])

    # Remove any white spaces [True/False]
    if 'strip' in conform:
        if conform['strip'] in true_list:
            if not isinstance(value, (string_types, binary_type)):
                raise ValueError('Can only [strip] Attribute Function to strings or binary types.')
            value = value.strip()

    # Converts String to Integer [True/False]
    if 'int' in conform:
        if conform['int'] in true_list:
            try:
                value = int(value)
            except:
                logging.warning('Cannot convert [%s] to integer.' % value)

    # Converts String to Integer [True/False]
    if 'float' in conform:
        if conform['float'] in true_list:
            try:
                value = float(value)
            except:
                logging.warning('Cannot convert [%s] to float.' % value)

    # Converts String to Integer [True/False]
    if 'text' in conform:
        value = conform['text']

    return value


def transform_fields(properties, conform):
    fields = OrderedDict()
    for key in conform.keys():
        value = None

        # STRING
        # Replace only a single field
        if isinstance(conform[key], (string_types, binary_type)):
            if conform[key] in properties:
                value = properties[conform[key]]
                value = clean_field(properties, conform[key])
            fields.update(dict([(key, value)]))

        # DICT
        # Replace & join multiple fields together
        elif isinstance(conform[key], (OrderedDict, dict)):
            value = clean_field(properties, conform[key])
            fields.update(dict([(key, value)]))

        # LIST
        # Join a values from a list
        elif isinstance(conform[key], (list, tuple)):
            value = clean_field(properties, conform[key])
            fields.update(dict([(key, value)]))

    return fields


def transform_columns(feature, config):
    config = read_config(config)
    conform = config['conform']
    feature['properties'] = transform_fields(feature['properties'], conform)

    return feature


if __name__ == "__main__":
    pass
