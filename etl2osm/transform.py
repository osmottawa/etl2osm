# -*- coding: utf-8 -*-

from __future__ import absolute_import
from osgeo import osr, ogr


def reproject(feature, crs, epsg=4326):
    # Source Projection
    p1 = osr.SpatialReference()
    p1.ImportFromWkt(crs)

    # Output Projection (WGS84)
    p2 = osr.SpatialReference()
    p2.ImportFromEPSG(epsg)

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


class Transform(object):
    def __init__(self, data, config, **kwargs):
        pass

if __name__ == "__main__":
    from extract import Extract

    infile = 'C:\Users\Claude\Downloads/test.shp'
    data = Extract(infile)
    print(data.crs)
    f = reproject(data[0], data.crs_wkt)
    print(f)
    # [-81.96776589029666, 28.957138814335224]
