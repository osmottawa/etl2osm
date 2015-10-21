ETL2OSM
=======

Extract, Transform and Load to OpenStreetMap

Installation
------------

GDAL & Fiona
~~~~~~~~~~~~

ETL2OSM depends on GDAL & Fiona, to install those packages using Windows.
Download the appropriate library from [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/) matching your Python version (Python27/34) & 64/32bit.

.. code:block:: bash

    $ cd packages
    $ pip install Fiona-1.6.2-cp27-none-win32.whl
    $ pip install GDAL-1.11.3-cp27-none-win32.whl


PyPi Install
~~~~~~~~~~~~

Install ETL2OSM from PyPi's online packages.

.. code:block:: bash

    $ pip install etl2osm


GitHub Install
~~~~~~~~~~~~~~

Install the latest version directly from Github.

.. code:block:: bash

    $ git clone https://github.com/osmottawa/etl2osm/
    $ cd etl2osm
    $ pip install .


Python API
----------

Step by Step doing a typical `Extract Transform Load` processing.

.. code:block:: python

    import etl2osm

    data = etl2osm.read(infile)
    data.transform(config)
    data.save(outfile)


Doing the entire process in a single line

.. code:block:: python

    etl2osm.process(infile, outfile=outfile, config=config)


To see what's happening, you can turn on the `Debug` mode.

.. code:block:: python

    etl2osm.process(infile, debug=True)


CLI API
-------

Reading the a file, the standard output will be in a GeoJSON format.

.. code:block:: bash

    $ etl2osm infile.shp --outfile outfile.osm --config config.json


Read & Transform the file using the config file.

.. code:block:: bash

    $ etl2osm infile.shp --config config.json


Entire process of `Extract Transform Load` to an OpenStreetMap format.

.. code:block:: bash

    $ etl2osm infile.shp --outfile outfile.osm --config config.json


Doing this process on multiple files using the `*` in your input file path.

Finds all the files starting with 2015 and ends with .kml

.. code:block:: bash

    $ etl2osm folder/2015*.shp --config config.json --format osm


To see what's happening, you can turn on the `Debug` mode.

.. code:block:: bash

    $ etl2osm infile.shp --debug


Examples of Config.json
-----------------------

Whenever you want to perform a transformation, include a config file in a JSON format.

Road Data
~~~~~~~~~

.. code:block:: json

    {
        "conform": {
            "type": "shapefile",
            "street": {
                "direction": "West",
                "basename": "Seminole",
                "suffix": "Avenue"
            },
            "maxspeed": {
                "mph": 45
            }
        }
    }


Address Data
~~~~~~~~~~~~

.. code:block:: json

    {
        "conform": {
            "type": "shapefile",
            "housenumber": 264,
            "street": {
                "basename": "Lawthorn",
                "suffix": "Street"
            },
            "postcode": 32162,
            "unit": 4
        }
    }
