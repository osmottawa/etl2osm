# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import logging
import fiona
from fiona.crs import from_epsg
import datetime
from etl2osm.transform import reproject, transform_columns, read_config



class Load(object):
    def __init__(self, data, **kwargs):

        # Default output file extenion to Shapefile
        if "outfile" in kwargs:
            outfile = kwargs.pop("outfile")
            extension = os.path.splitext(outfile)[1][1:]
        else:
            # If outfile path is not present, define it with the infile name
            if "infile" in kwargs: #append "_output" incase the input file is a shp file
                outfile = os.path.splitext(kwargs["infile"])[0] + "_output" + os.path.splitext(kwargs["infile"])[1]
                extension = "shp"
            else: #if not passed into function generate random name based on runtime
                outfile = "output_"+ datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
                extension = "shp"

        if 'config' in kwargs:
            config = read_config(kwargs.pop('config'))

        write_file = {
            'osm': self.write_osm,
            'geojson': self.write_geojson,
            'shp': self.write_shapefile,
            'kml': self.write_kml,
        }
        write_file[extension](data, outfile, config, **kwargs)

    def write_shapefile(self, data, outfile, config, **kwargs):
        """ Writes data to Shapefile format """

        # Data attributes from configuration file
        properties = dict((key, 'str') for key in config['conform'].keys())

        # Default Coordinate reference system is WGS84
        crs = from_epsg(4326)
        driver = 'ESRI Shapefile'
        encoding = 'utf-8'
        schema = data.schema
        schema['properties'] = properties

        with fiona.open(outfile, 'w', driver=driver, schema=schema, crs=crs, encoding=encoding) as sink:
            for feature in data:
                # Reproject data to WGS84 before saving
                feature = reproject(feature, data.crs_wkt, 4326)
                feature = transform_columns(feature, config)
                sink.write(feature)

    def write_osm(self, data, outfile, config, **kwargs):
        """ Writes data to OSM format """
        osm_id=1
        shape_nodeIDs=[]
        # Data attributes from configuration file
        properties = dict((key, 'str') for key in config['conform'].keys())

        # Default Coordinate reference system is WGS84
        crs = from_epsg(4326)
        driver = 'ESRI Shapefile'
        encoding = 'utf-8'
        schema = data.schema
        schema['properties'] = properties
        
        f_osm = open(outfile,"w")
        self.write_osm_header(f_osm)
        #write header
        for feature in data:
            # Reproject data to WGS84 before saving
            feature = reproject(feature, data.crs_wkt, 4326)
            feature = transform_columns(feature, config)
            #start by writing all the nodes
            if feature["geometry"]["type"]=="LineString":
                shape_nodeIDs=[]
                for node in feature["geometry"]["coordinates"]:
                    #write nodes
                    self.write_osm_node(f_osm,osm_id,node[1],node[0],feature["properties"])
                    shape_nodeIDs.append(osm_id)
                    osm_id+=1
                self.write_osm_way(f_osm,osm_id,shape_nodeIDs,feature["properties"])
                osm_id+=1
        f_osm.write("</osm>")
        f.close()    
        
        
        
        logging.info('Writing OSM: %s' % outfile)
        return ValueError('Writing OSM not implemented')

    def write_kml(self, data, outfile, config, **kwargs):
        """ Writes data to KML format """

        logging.info('Writing KML: %s' % outfile)
        return ValueError('Writing KML not implemented')

    def write_geojson(self, data, outfile, config, **kwargs):
        """ Writes data to GeoJSON format """

        logging.info('Writing GeoJSON: %s' % outfile)
        return ValueError('Writing GeoJSON not implemented')
    
    def write_osm_header(self,FileHandle,**kwargs):
        """ Writes JOSM xml header """
        FileHandle.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' upload='true' generator='JOSM'>\n")
    
    def write_osm_node(self,FileHandle,osm_id,latitude,longitude,properties,**kwargs):
        """ Writes JOSM xml node """
        FileHandle.write("  <node id='-" +str(osm_id)+ "' action='modify' visible='true' lat='"+str(latitude)+"' lon='"+str(longitude)+"'>\n")
        if ("number" in properties and "street" in properties): #might not exist
            if (not properties["number"]==None and not properties["street"]==None):
                #Both addr:housenumber and addr:street are required to be a valid address node
                FileHandle.write("    <tag k='addr:housenumber' v='"+ "{0:g}".format(properties["number"]) +"' />\n") 
                FileHandle.write("    <tag k='addr:street' v='" + properties["street"]+"' />\n")
                if "postcode" in properties:
                    if not properties["postcode"]==None:
                        FileHandle.write("    <tag k='addr:postcode' v='"+properties["postcode"]+"' />\n")
                if "unit" in properties:
                    if not properties["unit"]==None:
                        FileHandle.write("    <tag k='addr:unit' v='"+properties["unit"]+"' />\n")
                        FileHandle.write("    <tag k='ref' v='"+properties["unit"]+"' />\n")
        FileHandle.write("  </node>\n")
    
    def write_osm_way(self,FileHandle,osm_id,ref_nodes,properties,**kwargs):
        """ Writes JOSM xml segment """
        FileHandle.write("  <way id='-"+str(osm_id)+"' action='modify' visible='true'>\n")
        #Write nodes that belong to way(ids)
        for node in ref_nodes:
            FileHandle.write("    <nd ref='-"+str(node)+"' />\n")
        if not properties["street"]==None:
            FileHandle.write("    <tag k='name' v='"+properties["street"]+"' />\n")
            FileHandle.write("    <tag k='highway' v='road' />\n")
        
        FileHandle.write("  </way>\n")        
            
        

if __name__ == "__main__":
    pass
