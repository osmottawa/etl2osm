# -*- coding: utf-8 -*-
import os
import etl2osm
from osgeo import osr


root = os.path.dirname(etl2osm.__file__)[:-len('etl2osm')]


geojson = {
    'overlapping': os.path.join(root, "tests/geojson/overlapping.geojson"),
    'no-geometry': os.path.join(root, "tests/geojson/no-geometry.geojson")
}
shapefile = {
    'no-geometry': os.path.join(root, "tests/shapefile/no-geometry.shp"),
    'utm_projection': os.path.join(root, "tests/shapefile/utm_projection.shp")
}

roads = {
    'shp': os.path.join(root, "tests/shapefile/roads.shp"),
    'geojson': os.path.join(root, "tests/geojson/roads.geojson"),
    'geojson-blank': os.path.join(root, "tests/geojson/roads-blank.geojson"),
    'geojson-WGS84': os.path.join(root, "tests/geojson/roads-WGS84.geojson"),
    'geojson-zero': os.path.join(root, "tests/geojson/roads-zero.geojson"),
    'topojson': os.path.join(root, "tests/topojson/roads.topojson"),
    'kml': os.path.join(root, "tests/kml/roads.kml"),
    'osm': os.path.join(root, "tests/osm/roads.osm"),
    'unknown': os.path.join(root, "tests/geojson/roads"),
    'lake_county': os.path.join(root, "tests/shapefile/roads_lake_county.shp")
}

addresses = {
    'geojson': os.path.join(root, "tests/geojson/addresses.geojson"),
}

config = {
    'no-conform': os.path.join(root, "tests/config/no-conform.json"),
    'numbers': os.path.join(root, "tests/config/numbers.json"),
    'lake_county': {
        'roads': os.path.join(root, "tests/config/lake_county.json")
    },
}

wkt = osr.SRS_WKT_WGS84
epsg = 'EPSG:4326'
crs = {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
