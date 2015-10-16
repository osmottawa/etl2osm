#!/usr/bin/python
# coding: utf8

import re
import shapefile
from six import string_types, binary_type


lookup_suffix = {
    "US HWY": "US",
    "CR": "CR",
    "SR": "SR",
    "N": "North",
    "S": "South",
    "E": "East",
    "W": "West",
    "NE": "North East",
    "NW": "North West",
    "SE": "South East",
    "SW": "South West",
    "AVE": "Avenue",
    "BLVD": "Boulevard",
    "DR": "Drive",
    "LN": "Lane",
    "LOOP": "Loop",
    "PL": "Place",
    "RD": "Road",
    "TRL": "Trail",
    "TER": "Terrace",
    "Way": "Way",
    "CT": "Court",
    "CIR": "Circle",
    "ST": "Street",
}

cap_except = ["'s", "the", "in", "a", "CR", "US", "SR"]


def titlecase_except(s, exceptions=cap_except):
    word_list = re.split(' ', s)
    final = []
    for word in word_list:
        if word in exceptions:
            final.append(word)
        else:
            final.append(word.capitalize())
    return ' '.join(final)


def street_name(basename, suffix):
    return values

    # Remove any trailing white spaces
    street = street.strip()

    # Replace the suffix with lookup table
    if suffix:
        suffix = suffix.strip()
        if suffix in lookup_suffix:
            suffix = lookup_suffix[suffix]
        suffix = titlecase_except(suffix)

    # Titlecase the basename
    street = titlecase_except(street)

    # Join all fields together
    street_name = ' '.join([street, suffix])

    return street_name


def clean_feature(value):
    if isinstance(value, (string_types, binary_type)):
        return value.strip()
    return value


def process(infile, outfile, config):
    shp = shapefile.Reader(infile)

    # Get rid of extra garbage in field list
    # Remove the deletion flag from field list
    fields = list((i[0]) for i in shp.fields[1:])
 
    # Loop inside each feature within the Shapefile
    for feature in shp.iterShapeRecords():
        attributes = dict((fields[k], clean_feature(v)) for k, v in enumerate(feature.record))
        print(attributes)

if __name__ == '__main__':
    root = '/home/denis/Downloads/TheVillages/'
    infile = root + 'Sumter_Roads_WGS84.shp'
    outfile = root + 'Sumter_Roads_WGS84-EDIT.shp'
    config = {'addr:street': ['ST_NAME', 'ST_SUFFIX']}
    process(infile, outfile, config)
