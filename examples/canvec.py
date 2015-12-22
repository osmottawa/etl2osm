# -*- coding: utf-8 -*-

import os
import re
import etl2osm
from etl2osm import Models

models = Models()
path = '/home/denis/Downloads/canvec_021G_shp'

for root, dirs, files in os.walk(path):
    for file_name in files:
        if '.shp' in file_name:
            pattern = r'(?P<theme>[a-zA-Z]{2})_(?P<feature>\d+)_(?P<version>\d+)'
            match = re.search(pattern, file_name)
            if match:
                theme = models.canvecThemes.get(match.group('theme'))
                feature = models.canvecFeatures.get(int(match.group('feature')))
                version = match.group('version')
                if feature:
                    infile = os.path.join(root, file_name)
                    outfile = os.path.join(root, '{} - {}.shp'.format(theme, feature))
                    print 'Processing:', outfile
                    etl2osm.process(infile, outfile)
