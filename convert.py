#!/usr/bin/env python3
"""Convert address shapefile for address data
    Florida: The Villages
"""
import sys
import getopt
import shapefile
import copy
import re

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def usage():
    msg ="""usage: convert [-h (--help)] [-f (--file)] [-o (--output)]
    required arguments:
    -f, --file\t\tPath of shapefile to process
    -o, --output\t\tPath of output file"""
    print(msg)

def titlecase_except(s, exceptions):
    word_list = re.split(' ', s)       #re.split behaves as expected
    final =[]
    for word in word_list:
        if word in exceptions:
            final.append(copy.copy(word))
        else:
            final.append(copy.copy(word).capitalize())
    return " ".join(final)

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
        "NE":"North East",
        "NW":"North West",
        "SE":"South East",
        "SW":"South West",
        "AVE":"Avenue",
        "BLVD":"Boulevard",
        "DR":"Drive",
        "LN":"Lane",
        "LOOP":"Loop",
        "PL":"Place",
        "RD":"Road",
        "TRL":"Trail",
        "TER":"Terrace",
        "Way":"Way",
        "CT":"Court",
        "CIR":"Circle",
        "ST":"Street", 
    }
    return switcher.get(str_prefix,"UNDEFINED")

def street_suffix(str_suffix):
    if (str_suffix=="" or str_suffix.strip()==""):
        return ""
    switcher={
        "AVE":"Avenue",
        "BLVD":"Boulevard",
        "DR":"Drive",
        "LN":"Lane",
        "LOOP":"Loop",
        "PL":"Place",
        "RD":"Road",
        "TRL":"Trail",
        "TER":"Terrace",
        "Way":"Way",
        "CT":"Court",
        "CIR":"Circle",
        "ST":"Street", 
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

def write_header(file,minlat,minlon,maxlat,maxlon):
    file.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' upload='true' generator='JOSM'>\n")
    file.write("  <bounds minlat='"+ str(minlat) +"' minlon='"+ str(minlon) +"' maxlat='"+ str(maxlat) +"' maxlon='"+ str(maxlon) +"' origin='Sumter, Lake County' />\n")

def write_node(file,cntr,attr_list):
    #compile street
    street =""
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
    
    #start the output tag
    msg = "  <node id='-" + str(cntr) + "' action='modify' visible='true' lat='"+str(attr_list[6])+"' lon='"+str(attr_list[7])+"'>\n"
    msg +="    <tag k='addr:housenumber' v='"+str(attr_list[0])+"' />\n"
    msg +="    <tag k='addr:street' v='"+street.strip()+"' />\n"
    msg +="    <tag k='source:addr' v='Sumter, Lake County' />\n"
    msg +="    <tag k='addr:postcode' v='"+str(attr_list[5])+"' />\n"
    if not(attr_list[8] ==""):
        msg+="    <tag k='addr:unit' v='"+str(attr_list[8])+"' />\n"
        msg+="    <tag k='ref' v='" + str(attr_list[8])+"' />\n"
    msg +="  </node>\n"
    file.write(msg)

def process(infile,outfile):
    sf = shapefile.Reader(infile)
    fields=list(sf.fields)
    fields.pop(0) #remove the deletion flag from field list
    cntr=0   
    #remove extra garbage from field list
    new_list=[]
    for item in fields:
        new_list.append(item[0])
        
    fields=new_list
    new_list=None    
    rec = None
    
    f= open(outfile,'w')
    write_header(f,sf.bbox[1],sf.bbox[0],sf.bbox[3],sf.bbox[2])
    try:
        mega=[]
        for shapeRec in sf.iterShapeRecords():
            #check that the shape is a point and not a polygon
            attr_list=[]
            address=copy.copy(shapeRec.record[fields.index("AddressNum")])
            predir=copy.copy(shapeRec.record[fields.index("PrefixDire")])
            pretype=copy.copy(shapeRec.record[fields.index("PrefixType")])
            basestreet=copy.copy(shapeRec.record[fields.index("BaseStreet")])
            suffix=copy.copy(shapeRec.record[fields.index("SuffixType")])
            zipcode=copy.copy(shapeRec.record[fields.index("ZipCode")])
            unitnum= copy.copy(shapeRec.record[fields.index("UnitNumber")])
            lat=copy.copy(shapeRec.shape.points[0][1])
            long=copy.copy(shapeRec.shape.points[0][0])
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
                    attr_list.append(basestreet.decode("utf-8"))
                else:
                    attr_list.append(basestreet)
            except:
                attr_list.append("")
            
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
        sf=None
        f.close()    
    except:
        print (sys.exc_info()[0])
        f.close()
        
    return 0

def main(argv=None):
    shpfile=None
    outputfile=None
    FileType="Lake"
    if argv is None:
        argv=sys.argv;
    try:
        try:
            opts,args = getopt.getopt(argv[1:], 'hlsf:o:', ["help","file=","output=","lakecounty","sumtercounty"])
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
        elif opt in ("-l","--lakecounty"):
            FileType="Lake"
        elif opt in ("-s","--sumtercounty"):
            FileType="Sumter"
        else:
            usage()
            return 2
        #process the information
    if FileType=="Lake":
        return process(shpfile,outputfile)
    elif FileType=="Sumter":
        return 0
    

if __name__ == "__main__":
    sys.exit(main())
        
    
        
