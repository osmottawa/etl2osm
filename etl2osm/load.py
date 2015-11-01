# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import json
import logging
import fiona
from fiona.crs import from_epsg
from lxml import etree


class Load(object):
    def save(self, outfile):
        """ Saves file to path """

        extension = os.path.splitext(outfile)[1][1:]
        write_file = {
            'osm': self.write_osm,
            'geojson': self.write_geojson,
            'shp': self.write_shapefile,
            'kml': self.write_kml,
        }
        write_file[extension](outfile)

    def write_shapefile(self, outfile):
        """ Writes data to Shapefile format """

        # Default Coordinate reference system is WGS84
        crs = from_epsg(4326)
        driver = 'ESRI Shapefile'
        encoding = 'utf-8'
        schema = {
            'geometry': self.geometry,
            'properties': self.properties
        }

        with fiona.open(outfile, 'w', driver=driver, schema=schema, crs=crs, encoding=encoding) as sink:
            for feature in self.features:
                sink.write(feature)

    def write_geojson(self, outfile):
        """ Writes data to GeoJSON format """

        logging.info('Writing GeoJSON: %s' % outfile)

        with open(outfile, 'wb') as f:
            f.write(json.dumps(self.geojson, indent=4))

    def write_osm(self, outfile):
        """ Writes data to OSM format """

        logging.info('Writing OSM: %s' % outfile)
        osm = etree.Element("osm", version="0.6", upload="false", generator="etl2osm")
        osm_id = -1

        for feature in self.features:
            geometry = feature['geometry']
            coordinates = geometry['coordinates']

            # Handle Node
            if geometry['type'] == 'Point':
                osm_id -= 1
                node = etree.Element(
                    "node",
                    id=str(osm_id),
                    action='modify',
                    visible='true',
                    lat=str(coordinates[1]),
                    lon=str(coordinates[0]),
                )
                # Add tag attributes to node
                for key, value in feature['properties'].items():
                    etree.SubElement(node, "tag", k=key, v=str(value))

                # Add node to OSM
                osm.append(node)

            # Handle Way
            if geometry['type'] == 'LineString':
                osm_id -= 1
                way = etree.Element(
                    "way",
                    id=str(osm_id),
                    action='modify',
                    visible='true',
                )

                # Add tag attributes to way
                for key, value in feature['properties'].items():
                    etree.SubElement(way, "tag", k=key, v=str(value))

                # Get Refence Nodes
                for coordinate in feature["geometry"]["coordinates"]:
                    osm_id -= 1
                    etree.SubElement(
                        osm,
                        "node",
                        id=str(osm_id),
                        visible='true',
                        lon=str(coordinate[0]),
                        lat=str(coordinate[1])
                    )
                    etree.SubElement(way, "nd", ref=str(osm_id))
                osm.append(way)

        with open(outfile, 'wb') as f:
            f.write(etree.tostring(osm, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

    def write_kml(self, outfile):
        """ Writes data to KML format """

        logging.info('Writing KML: %s' % outfile)
        raise ValueError('Writing KML not implemented')
