Map tiles for BlueSky!
===================================

This is a tutorial that will explain how to:

#. create custom map tiles.
#. create a tile server.
#. create a custom style with custom tiles.
#. serve the tiles to `BlueSky <https://github.com/TUDelft-CNS-ATM/bluesky/>`_.

We will make the map tiles that are used for the `Metropolis-2 <https://metropolis2.eu/>`_ simulations.

.. note::

   This project is under active development.

Requirements
--------------

This tutorial will use several open source projects:

#. `QGIS <https://github.com/qgis/QGIS>`_
#. `OpenMapTiles <https://github.com/openmaptiles/openmaptiles>`_
#. `tippecanoe <https://github.com/mapbox/tippecanoe>`_
#. `maputnik <https://github.com/maputnik/editor>`_
#. `TileServer GL <https://github.com/maptiler/tileserver-gl>`_

Please refer to the documentation of each project for help on installation and usage.

Contents
--------

.. toctree::
   :maxdepth: 2
   
   tiles
   server
   style
   bluesky
