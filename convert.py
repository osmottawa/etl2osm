#!/usr/bin/env python3
"""Convert address shapefile for address data
    Florida: The Villages
"""
import sys
import getopt
import shapefile
import copy
import re
import json

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def usage():
    msg ="""usage: convert [-h (--help)] [-f (--file)] [-o (--output)]
    required arguments:
    -f, --file\t\tPath of shapefile to process
    -o, --output\t\tPath of output file
    -c, --config\t\tConfig file for columns"""
    print(msg)

def titlecase_except(s, exceptions):
    word_list = re.split(' ', s)
    final = []
    for word in word_list:
        if word in exceptions:
            final.append(word)
        else:
            final.append(word.capitalize())
    return " ".join(final)

def process_basestreet(street):
    if re.match("^C-",street):
        street = "CR " + street[2:]
    elif re.match("^I\d",street):
        street="I " + street[1:]
    return street

def street_prefix(str_prefix):
    if (str_prefix=="" or str_prefix.strip()==""):
        return ""
    switcher={
        "US HWY":"US",
        "CR":"CR",
        "SR":"SR",
        "N":"North",
        "S":"South",
        "E":"East",
        "W":"West",
        "NE":"Northeast",
        "NW":"Northwest",
        "SE":"Southeast",
        "SW":"Southwest"        
    }
    return switcher.get(str_prefix,"UNDEFINED")

def street_suffix(str_suffix):
    if (str_suffix=="" or str_suffix.strip()==""):
        return ""
    switcher={
        "ALY":"Alley",
        "ANX":"Annex",
        "ARC":"Arcade",
        "AVE":"Avenue",
        "YU":"Bayou",
        "BCH":"Beach",
        "BND":"Bend",
        "BLF":"Bluff",
        "BTM":"Bottom",
        "BLVD":"Boulevard",
        "BR":"Branch",
        "BRG":"Bridge",
        "BRK":"Brook",
        "BG":"Burg",
        "BYP":"Bypass",
        "CP":"Camp",
        "CYN":"Canyon",
        "CPE":"Cape",
        "CSWY":"Causeway",
        "CTR":"Center",
        "CIR":"Circle",
        "CLFS":"Cliffs",
        "CLB":"Club",
        "COR":"Corner",
        "CORS":"Corners",
        "CRSE":"Course",
        "CT":"Court",
        "CTS":"Courts",
        "CV":"Cove",
        "CRK":"Creek",
        "CRES":"Crescent",
        "XING":"Crossing",
        "DL":"Dale",
        "DM":"Dam",
        "DV":"Divide",        
        "DR":"Drive",
        "DR S":"Drive South",
        "EST":"Estates",
        "EXPY":"Expressway",
        "EXT":"Extension",
        "FALL":"Fall",
        "FLS":"Falls",
        "FRY":"Ferry",
        "FLD":"Field",
        "FLDS":"Fields",
        "FLT":"Flats",
        "FOR":"Ford",
        "FRST":"Forest",
        "FGR":"Forge",
        "FORK":"Fork",
        "FRKS":"Forks",
        "FT":"Fort",
        "FWY":"Freeway",
        "GDNS":"Gardens",
        "GTWY":"Gateway",
        "GLN":"Glen",
        "GN":"Green",
        "GRV":"Grove",
        "HBR":"Harbor",
        "HVN":"Haven",
        "HTS":"Heights",
        "HWY":"Highway",
        "HL":"Hill",
        "HLS":"Hills",
        "HOLW":"Hollow",
        "INLT":"Inlet",
        "IS":"Island",
        "ISS":"Isle",
        "JCT":"Juction",
        "CY":"Key",
        "KNLS":"Knolls",
        "LK":"Lake",
        "LKS":"Lakes",
        "LNDG":"Landing",
        "LN":"Lane",
        "LGT":"Light",
        "LF":"Loaf",
        "LCKS":"Locks",
        "LDG":"Lodge",
        "LOOP":"Loop",
        "MALL":"Mall",
        "MNR":"Manor",
        "MDWS":"Meadows",
        "ML":"Mill",
        "MLS":"Mills",
        "MSN":"Mission",
        "MT":"Mount",
        "MTN":"Mountain",
        "NCK":"Neck",
        "ORCH":"Orchard",
        "OVAL":"Oval",
        "PARK":"Park",
        "PKY":"Parkway",
        "PASS":"Pass",
        "PATH":"Path",
        "PIKE":"Pike",
        "PNES":"Pines",
        "PL":"Place",
        "PLN":"Plain",
        "PLNS":"Plains",
        "PLZ":"Plaza",
        "PT":"Point",
        "PRT":"Port",
        "PR":"Prairie",
        "RADL":"Radial",
        "RNCH":"Ranch",
        "RPDS":"Rapids",
        "RST":"Rest",
        "RDG":"Ridge",
        "RIV":"River",
        "RD":"Road",
        "ROW":"Row",
        "RUN":"Run",
        "SHL":"Shoal",
        "SHLS":"Shoals",
        "SHR":"Shore",
        "SHRS":"Shores",
        "SPG":"Spring",
        "SPGS":"Springs",
        "SPUR":"Spur",
        "SQ":"Square",
        "STA":"Station",
        "STRA":"Stravenues",
        "STRM":"Stream",
        "ST":"Street",
        "SMT":"Sommit",
        "TER":"Terrace",
        "TRCE":"Trace",
        "TRAK":"Track",
        "TRL":"Trail",
        "TRLR":"Tailer",
        "TUNL":"Tunnel",
        "TPKE":"Turnpike",
        "UN":"Union",
        "VLY":"Valley",
        "VIA":"Viaduct",
        "VW":"View",
        "VLG":"Village",
        "VL":"Ville",
        "VIS":"Vista",
        "WALK":"Walk",
        "Way":"Way",
        "WLS":"Wells"
    }
    return switcher.get(str_suffix,"UNDEFINED")

def unit_num(unit):
    if (unit=="" or unit.strip()==""):
        return ""
    tmpstr=""
    if ("&" in unit):
        pre=unit[:unit.find("&")] #preamble
        tmpstr+=pre + ";"
        items=unit.split("&")
        if ("&amp;" in unit):
            items=unit.split("&amp;")            
        items.pop(0) #remove the pre from list
        for item in items:
            tmpstr += pre[:len(item)*-1]+str(item) + ";" #substring pre for length of item
        tmpstr=tmpstr[:len(tmpstr)-1]#remove extra ;   
    return tmpstr        

def write_closer(file):
    file.write("</osm>")

def write_header(file,bbox):
    file.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' upload='true' generator='JOSM'>\n")
    file.write("  <bounds minlat='"+ str(bbox[1]) +"' minlon='"+ str(bbox[0]) +"' maxlat='"+ str(bbox[3]) +"' maxlon='"+ str(bbox[2]) +"' origin='Sumter, Lake County' />\n")

def write_node(file,cntr,attr_list):
    #start the output tag
    msg = "  <node id='-" + str(cntr) + "' action='modify' visible='true' lat='"+str(attr_list[6])+"' lon='"+str(attr_list[7])+"'>\n"
    
    #compile street
    street =""    
    if not (attr_list[2].strip()=="" and attr_list[3].strip()=="" and attr_list[4].strip()==""):
        #if len(attr_list[1])>1:
        #    street+=attr_list[1]+" " #direction of street not needed in name
        if len(attr_list[2])>1:
            street+=attr_list[2]+" "
        if len(attr_list[3])>1:
            street+=attr_list[3]+" "
        if len(attr_list[4])>1:
            street+=attr_list[4]
        #words we don't want capitalized
        cap_except =["'s","the","in","a","CR","US","SR"]
        street = titlecase_except(street,cap_except)
        msg +="    <tag k='addr:street' v='"+street.strip()+"' />\n"
    
    if not (attr_list[0]==None):
        msg +="    <tag k='addr:housenumber' v='"+ "{0:g}".format(attr_list[0]) +"' />\n"
    
    msg +="    <tag k='source:addr' v='Sumter, Lake County' />\n"
    
    if not(attr_list[5]==None):
        msg +="    <tag k='addr:postcode' v='"+ "{0:g}".format(attr_list[5])+"' />\n"
    
    if not(attr_list[8] ==""):
        msg+="    <tag k='addr:unit' v='"+str(attr_list[8])+"' />\n"
        msg+="    <tag k='ref' v='" + str(attr_list[8])+"' />\n"
    msg +="  </node>\n"
    file.write(msg)

def process(infile,outfile,jConfig):
    #
    shp = shapefile.Reader(infile)
    #get rid of extra garbage in field list
    #remove the deletion flag from field list
    fields = list((i[0]) for i in shp.fields[1:])

    cntr=0
        
    f= open(outfile,'w')
    write_header(f,shp.bbox)
    try:
        for feature in shp.iterShapeRecords():
            #check that the shape is a point and not a polygon
            attr_list=[]
            pbasestreet=False
            address=""
            if "Number" in jConfig:
                address=copy.copy(feature.record[fields.index(jConfig["Number"])])
            predir=""
            if "PrefixDir" in jConfig["StreetName"]:
                predir=copy.copy(feature.record[fields.index(jConfig["StreetName"]["PrefixDir"])])
            pretype=""
            if "Prefix" in jConfig["StreetName"]:
                pretype=copy.copy(feature.record[fields.index(jConfig["StreetName"]["Prefix"])])
            basestreet=""
            if "Name" in jConfig["StreetName"]:
                basestreet=copy.copy(feature.record[fields.index(jConfig["StreetName"]["Name"])])
            suffix=""
            if "Suffix" in jConfig["StreetName"]:
                suffix=copy.copy(feature.record[fields.index(jConfig["StreetName"]["Suffix"])])
            zipcode=""
            if "Postal" in jConfig:
                zipcode=copy.copy(feature.record[fields.index(jConfig["Postal"])])
            unitnum=""
            if "Unit" in jConfig:
                unitnum= copy.copy(feature.record[fields.index(jConfig["Unit"])])
            lat=copy.copy(feature.shape.points[0][1])
            long=copy.copy(feature.shape.points[0][0])
            
            #Street Name might be all in one string
            if not("PrefixDir" in jConfig["StreetName"] or "Prefix" in jConfig["StreetName"]):
                pbasestreet=True
            
            
            #Address- 0
            attr_list.append(address)
            #Street Name - 1 2 3 4
            try:
                if isinstance(predir,bytes):
                    attr_list.append(street_prefix(predir.decode("utf-8")))
                else:
                    attr_list.append(street_prefix(predir))
            except:
                attr_list.append("")
            try:
                if isinstance(pretype,bytes):
                    attr_list.append(street_prefix(pretype.decode("utf-8")))
                else:
                    attr_list.append(street_prefix(pretype))
            except:
                attr_list.append("")
            
            try:
                if isinstance(basestreet,bytes):
                    basestreet=basestreet.decode("utf-8")
            except:
                basestreet=""
            if pbasestreet:
                basestreet=process_basestreet(basestreet)
            attr_list.append(basestreet)
            
            try:
                if isinstance(suffix,bytes):
                    attr_list.append(street_suffix(suffix.decode("utf-8")))
                else:
                    attr_list.append(street_suffix(suffix))
            except:
                attr_list.append("")
            
            #ZipCode -5
            try:
                if isinstance(zipcode,bytes):
                    attr_list.append(zipcode.decode("utf-8"))
                else:
                    attr_list.append(zipcode)
            except:
                    attr_list.append("")
            #Latitude - 6
            attr_list.append(lat)
            #Longitude -7
            attr_list.append(long)
            #UnitNumber -8
            try:
                if isinstance(unitnum,bytes):
                    attr_list.append(unit_num(unitnum.decode("utf-8").strip()))
                else:
                    attr_list.append(unit_num(unitnum.strip()))
            except:
                attr_list.append("")
            cntr+=1
            if cntr>1:
                print('\b'*len(str(cntr-1)),end='')
                print(cntr)
            else:
                print(cntr)
            sys.stdout.flush()
            write_node(f,cntr,attr_list)           
        
        write_closer(f)
        shp=None
        f.close()    
    except:
        print (sys.exc_info()[0])
        f.close()
        
    return 0

def main(argv=None):
    shpfile=None
    outputfile=None
    configfile=None
    
    if argv is None:
        argv=sys.argv;
    try:
        try:
            opts,args = getopt.getopt(argv[1:], 'hc:f:o:', ["help","file=","output=","config"])
        except getopt.error as msg:
            raise Usage(msg)
        #more code
    except Usage as err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    for opt,arg in opts:
        if opt in ("-h","--help"):
            usage()
            return 2
        elif opt in ("-f","--file"):
            shpfile=arg
        elif opt in ("-o","--output"):
            outputfile=arg
        elif opt in ("-c","--config"):
            configfile=arg
        else:
            usage()
            return 2

    #get config
    data = open(configfile).read();
    if isinstance(data,bytes):
        data=data.decode("utf-8") #don't want byte strings
    jConfig=json.loads(data)
    
    #process the information    
    if jConfig["Type"]=="Address":
        return process(shpfile,outputfile,jConfig)
    elif jConfig["Type"]=="Roads":
        return 0     

if __name__ == "__main__":
    sys.exit(main())