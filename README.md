ETL2OSM
=======

Extract, Transform and Load to OpenStreetMap

[![Build Status](https://travis-ci.org/osmottawa/etl2osm.svg?branch=master)](https://travis-ci.org/osmottawa/etl2osm)
[![Coverage Status](https://coveralls.io/repos/osmottawa/etl2osm/badge.svg?branch=master&service=github)](https://coveralls.io/github/osmottawa/etl2osm?branch=master)

Features
--------

- Extracts & Loads data from multiple formats:

  - Shapefile
  - GeoJSON
  - OSM
  - KML (Coming Soon)

- Replace direction fields (NE > Northeast, SW > Southwest)
- Replace street suffix fields (AVE > Avenue, ST > Street)
- Change & remove attribute names
- Convert text fields into proper titlecase (ottawa ONTARIO > Ottawa Ontario)
- Transform data into WGS84 (EPSG:4326)


API Overview
------------

Step by Step doing a typical `Extract Transform Load` processing.

```python
>>> import etl2osm
>>> data = etl2osm.extract("infile.shp")
>>> data.transform("config.json")
>>> data.save("outfile.osm")
```

Doing the entire process in a single line

```python
>>> import etl2osm
>>> etl2osm.process("infile.shp", "config.json", "outfile.osm")
```

Command Line Interface
----------------------

Reading the a file, the standard output will be in a GeoJSON format.

```bash
$ etl2osm "infile.shp" --config "config.json" --outfile "outfile.osm"
```

See [Examples](https://github.com/osmottawa/etl2osm/tree/master/examples) for more information.

Making a Config.json
--------------------

Whenever you want to perform a transformation, include a config file in a JSON format.

### Road Data

```json
{
    "conform": {
        "addr:street": [
            {"function": "direction", "field":"DIRECTION"},
            {"function": "title", "field": "ST_NAME"},
            {"function": "suffix", "field": "ST_EXT"}
        ],
        "maxspeed": {"function": "mph", "field": "Speed_Limi"}
    }
}
```

### Address Data

```json
{
    "conform": {
        "addr:number": {"int": "True", "field": "NUMBER_"},
        "addr:street": [
            {"function": "direction", "field": "PREDIR"},
            {"function": "title", "field": "ST_NAME"},
            {"function": "suffix", "field": "STSUFFIX"}
        ],
        "addr:postcode": {"int": "True", "field": "ZIP_CODES"},
        "addr:unit": "UNIT"
    }
}
```

Installation
------------

### GDAL & Fiona

ETL2OSM depends on GDAL, Fiona & LXML; to install those packages using Windows.
Download the appropriate library from [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/) matching your Python version (Python27/34) & 64/32bit.

```bash
$ cd packages
$ pip install lxml‑3.4.4‑cp27‑none‑win32.whl
$ pip install Fiona-1.6.2-cp27-none-win32.whl
$ pip install GDAL-1.11.3-cp27-none-win32.whl
```

### PyPi Install

Install ETL2OSM from PyPi's online packages.

```bash
$ pip install etl2osm
```

### GitHub Install

Install the latest version directly from Github.

```bash
$ git clone https://github.com/osmottawa/etl2osm/
$ cd etl2osm
$ pip install .
```
