# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import logging
from etl2osm.models import Models
from six import string_types, binary_type
from collections import OrderedDict
from osgeo import osr, ogr


true_list = ['True', 'true', '1', True, 1]
models = Models()
POINT = ogr.Geometry(ogr.wkbPoint)
SpatialReferenceType = osr.SpatialReference().__class__


def confirm_geometry(feature):
    geom = feature['geometry']
    coord = geom['coordinates']

    if feature['geometry']['type'] == 'MultiPoint':
        if len(coord) == 1:
            feature['geometry']['coordinates'] = coord[0]
            feature['geometry']['type'] = 'Point'
            logging.warning('Geometry changed: MultiPoint >> Point.')
    return feature


def regex_strip(value):
    # ESRI Shapfiles have fields [SUB] blank fields at the end
    # Regex will search all characters but must END with a letter or number
    # Also acts as an .strip() function
    if isinstance(value, (string_types, binary_type)):
        match = re.search(r'^([a-z,A-Z,0-9].+[a-z,A-Z,0-9])', value)
        if match:
            value = match.group()
    return unicode(value)


def config_to_properties(config):
    properties = OrderedDict()

    for key, value in config.items():
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
        # If no source projection is present, it will assume WGS84 (EPSG:4326)
        valid = projection.ImportFromEPSG(4326)
        logging.warning('Cannot detect the type Coordinate Reference System (CRS)')

    # Check if results are valid (0 == Valid projection)
    if not valid == 0:
        raise ValueError('EPSG provided was invalid for CRS: {0}'.format(crs))

    logging.info('Get CRS: %s' % projection)
    return projection


def extract_epsg(crs):
    if isinstance(crs, (string_types, binary_type)):
        pattern = r'(epsg|EPSG):\D*(?P<epsg>\d+)'
        match = re.search(pattern, crs)
        if match:
            return int(match.group('epsg'))

    if isinstance(crs, dict):
        if crs['type'] == 'name':
            if 'properties' in crs:
                return extract_epsg(crs['properties']['name'])
            else:
                return extract_epsg(crs['name'])
    return crs


def reproject(feature, crs_source, crs_target=4326, **kwargs):
    # Source Projection
    if isinstance(crs_source, SpatialReferenceType):
        p1 = crs_source
    else:
        p1 = get_coordinate_rerefence_system(extract_epsg(crs_source))

    # Output Projection (WGS84)
    if isinstance(crs_source, SpatialReferenceType):
        p2 = crs_target
    else:
        p2 = get_coordinate_rerefence_system(extract_epsg(crs_target))

    # Define Coordinate Transformation
    coord_trans = osr.CoordinateTransformation(p1, p2)

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
    feature['geometry']['coordinates'] = convert[geom['type']](p1, p2, coord, coord_trans)

    return feature


def convert_point(p1, p2, coord, coord_trans=''):
    # Add point to GDAL point schema
    POINT.AddPoint(coord[0], coord[1])

    # Only reproject if projections are different
    if not p1.IsSame(p2):
        if not coord_trans:
            coord_trans = osr.CoordinateTransformation(p1, p2)
        POINT.Transform(coord_trans)

    return POINT.GetPoint_2D()


def convert_multi_point(p1, p2, coord, coord_trans=''):
    multi_point = []
    for point in coord:
        multi_point.append(convert_point(p1, p2, point, coord_trans))

    return multi_point


def convert_multi_linestring(p1, p2, coord, coord_trans=''):
    multi_line = []
    for line in coord:
        multi_line.append(convert_linestring(p1, p2, line, coord_trans))

    return multi_line


def convert_linestring(p1, p2, coord, coord_trans=''):
    line = []
    for point in coord:
        line.append(convert_point(p1, p2, point, coord_trans))

    return line


def convert_polygon(p1, p2, coord, coord_trans=''):
    polygon = []
    for line in coord:
        polygon.append(convert_linestring(p1, p2, line, coord_trans))

    return polygon


def titlecase_except(value, **kwargs):
    if isinstance(value, (string_types, binary_type)):
        word_list = re.split(' ', value)
        final = []

        for word in word_list:
            if word in models['title_except']:
                final.append(word)
            else:
                final.append(word.capitalize())

        return ' '.join(final)
    return value


def clean_field(properties, config, **kwargs):
    # Standalone Text as Field
    if isinstance(config, (string_types, binary_type)):
        if config not in properties:
            logging.warning('Cannot find attribute [%s] using the Attribute Function.' % config)
        value = properties.get(config)
    elif isinstance(config, list):
        message = 'Cannot clean a list'
        raise ValueError(message)
    else:
        # REQUIRED: Define value using [field]
        if 'field' in config:
            if config['field'] not in properties:
                logging.warning('Cannot find attribute [%s] using the Attribute Function.' % config)
            value = properties.get(config['field'])

        # Simple hard coded text
        elif 'text' in config:
            value = config['text']
        else:
            message = 'Config must contain at least [field] OR [text].'
            raise ValueError(message)

        if 'model' in config:
            if config['model'] in models:
                model = models[config['model']]
            else:
                model = Models(config['model'])
            value = model.get(properties.get(config['field']))

        # Converts string to a nice Titlecase (3RD AVENUE=3rd Avenue)
        if config.get('title'):
            value = titlecase_except(value)

    return value


def transform_fields(properties, config, **kwargs):
    fields = OrderedDict()
    for key in config.keys():
        value = None

        # STRING
        # Replace only a single field
        if isinstance(config[key], (string_types, binary_type)):
            if config[key] in properties:
                value = properties[config[key]]
                value = clean_field(properties, config[key], **kwargs)
            fields.update(dict([(key, value)]))

        # DICT
        # Replace & join multiple fields together
        elif isinstance(config[key], (OrderedDict, dict)):
            value = clean_field(properties, config[key], **kwargs)
            fields.update(dict([(key, value)]))

        # LIST
        # Join a values from a list
        elif isinstance(config[key], (list, tuple)):
            items = []
            for item in config[key]:
                value = clean_field(properties, item, **kwargs)
                if value:
                    items.append(value)
            fields.update(dict([(key, " ".join(items))]))

    return fields


def transform_columns(feature, config, **kwargs):
    feature['properties'] = transform_fields(feature['properties'], config, **kwargs)

    return feature


if __name__ == "__main__":
    pass
