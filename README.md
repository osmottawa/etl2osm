ETL2OSM
=======

Extract, Transform and Load to OpenStreetMap

Installation
------------

### GDAL & Fiona

ETL2OSM depends on GDAL & Fiona, to install those packages using Windows.
Download the appropriate library from [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/) matching your Python version (Python27/34) & 64/32bit.

```bash
$ cd packages
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
$ python setup.py install
```

Getting Started
---------------

Converting your KML file into a ESRI compatible Shapefile.

```bash
$ etl2osm filepath/example.kml --format shp
```

Saving output as a specific name `newfile` into both Shapefile & GeoJSON format.

```bash
$ etl2osm example.kml --out newfile --format shp
$ etl2osm example.kml --out newfile --format geojson
```

Convert multiple files using the `*` in your input file path.

```bash
# Finds all the files starting with 2015 and ends with .kml

$ etl2osm folder/2015*.kml --format shp
```

To see what's happening, you can turn on the `Debug` mode.

```bash
$ etl2osm example.shp --debug
```


Schema
------

Upload your address & road dataset into `source` as a JSON file.

### Roads

```json
{
	"street": {
	    "direction": "West",
	    "basename": "Seminole",
	    "suffix": "Avenue"
	},
	"maxspeed": {
	    "mph": 45
	}
}
```

### Address

```json
{
    "housenumber": 264,
    "street": {
        "basename": "Lawthorn",
        "suffix": "Street"
    },
    "postcode": 32162,
    "unit": 4
}
```