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


def get_coordinate_rerefence_system(crs):
    projection = osr.SpatialReference()

    # Read Projection from EPSG or WKT
    # For all EPSG projections
    # http://spatialreference.org/ref/epsg/wgs-84/
    if isinstance(crs, int):
        valid = projection.ImportFromEPSG(crs)

    elif isinstance(crs, (string_types, binary_type)):
        valid = projection.ImportFromWkt()
    else:
        raise ValueError('Cannot detect the type Coordinate Reference System (CRS)')

    # Check if results are valid (0 == Valid projection)
    if valid == 0:
        logging.info('Get CRS: %s' % projection)
        return projection
    else:
        raise ValueError('EPSG provided was invalid for CRS: {0}'.format(crs))


def reproject(feature, crs_source, crs_target=4326):
    # Source Projection
    p1 = get_coordinate_rerefence_system(crs_source)

    # Output Projection (WGS84)
    p2 = get_coordinate_rerefence_system(crs_target)

    geom = feature['geometry']
    coord = feature['geometry']['coordinates']

    convert = {
        'Point': convert_point,
        'LineString': convert_linestring,
        'Polygon': convert_polygon,
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


def convert_linestring(p1, p2, coord):
    line = []
    for point in coord:
        line.append(convert_point(p1, p2, point))
    return line


def convert_polygon(p1, p2, coord):
    polygon = []
    for line in coord:
        polygon.append(convert_linestring(line))
    return polygon


def read_config(config):
    if isinstance(config, dict):
        return config
    if not os.path.exists(config):
        raise ValueError('Config file path does not exist: %s' % config)
    with open(config) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def titlecase_except(value, exceptions=cap_except):
    word_list = re.split(' ', value)
    final = []
    for word in word_list:
        if word in exceptions:
            final.append(word)
        else:
            final.append(word.capitalize())
    return ' '.join(final)


def clean_field(value, key, sub_key=''):
    if isinstance(value, (string_types, binary_type)):
        value = value.strip()

    if sub_key == 'suffix':
        if value in suffix:
            return suffix[str(value)]
    elif sub_key == 'direction':
        if value in direction:
            return direction[str(value)]
    elif sub_key == 'title':
        return titlecase_except(value)
    elif sub_key == 'int':
        return str(int(value))
    elif sub_key == 'mph':
        return '{0} mph'.format(value)
    return value


def transform_fields(properties, conform):
    fields = OrderedDict()
    for key in conform.keys():
        value = None

        # Replace only a single field
        if isinstance(conform[key], (string_types, binary_type)):
            if conform[key] in properties:
                value = properties[conform[key]]
                value = clean_field(value, key)
            fields.update(dict([(key, value)]))

        # Replace & join multiple fields together
        elif isinstance(conform[key], OrderedDict):
            values = []
            for sub_key in conform[key]:
                if conform[key][sub_key] in properties:
                    value = properties[conform[key][sub_key]]
                    if value:
                        values.append(clean_field(value, key, sub_key))

            # Join all fields together to make new value
            value = ' '.join(values)
            fields.update(dict([(key, value)]))

        elif isinstance(conform[key], (list, tuple)):
            values = []
            for k in conform[key]:
                if isinstance(k, dict):
                    for sub_key, k in k.items():
                        if k in properties:
                            value = properties[k]
                            if value:
                                value = clean_field(value, k, sub_key)
                                values.append(value)

                elif isinstance(k, (string_types, binary_type)):
                    if k in properties:
                        if properties[k]:
                            value = clean_field(properties[k], key)
                            values.append(value)

            # Join all fields together to make new value
            value = ' '.join(values)
            fields.update(dict([(key, value)]))
    return fields


def transform_columns(feature, config):
    config = read_config(config)
    conform = config['conform']
    feature['properties'] = transform_fields(feature['properties'], conform)
    return feature


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    feature = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [100.0, 0.5]}
    }
    feature2 = reproject(feature, 4326, 4326)
    print(feature == feature2)
    print(feature2)
