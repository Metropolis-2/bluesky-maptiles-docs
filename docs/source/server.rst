Serving the tiles
===================================

The goal of this section is to serve as a general tutorial of how to work with 
OpenMaptiles, TileServer GL, and maputnik. This will for sure not be an comprehensive tutorial and
will only show enough for our purposes.

Working with OpenMapTiles and TileServer GL
----------------------------------------------
Per their documentation "OpenMapTiles is an extensible and open tile schema based on the OpenStreetMap. 
This project is used to generate vector tiles for online zoomable maps. 
OpenMapTiles is about creating a beautiful basemaps with general layers containing topographic information".

OpenMapTiles provides a simple way to download OSM data and create maps. In simple words they convert OSM data
into :code:`mbtiles`. OpenMapTiles organizes the vector tiles into a `schema <https://openmaptiles.org/schema/>`_ that
makes it simple to style. It is also possible to make custom layers from OSM data. `Here <https://github.com/openmaptiles/openmaptiles-skiing>`_ 
is a nice example.

However, for this tutorial we won't really focus on these capabilties as we do not want our data to come directly from OSM. 
In Metropolis-2, we modified streets and buildings to ensure they are usable in BlueSky.
Downloading OpenMapTiles also brings TileServer GL. It is also possible to skip OpenMapTiles and just 
download TileServer GL but we will not. Note that both will require installing `docker <https://www.docker.com/>`_.

Start the server
*****************
OpenMapTiles brings in a lot of `commands <https://github.com/openmaptiles/openmaptiles#develop>`_ that are used for creating and
serving the tiles. To create a tile server it is as simple as just running :code:`make start-tileserver` in the root directory
of :code:`openmaptiles`. This should give you something similar to this:

.. image:: ../images/startserver.png
   :width: 900

The output gives us a couple clues as to how the tile server works.

* The tile server is at :code:`http://localhost:8080`.
* A docker command is executed :code:`docker run --rm --user=501:20 -it --name tileserver-gl -v $(pwd)/data:/data -p 8080:8080 maptiler/tileserver-gl --port 8080`
* No :code:`mbtiles` file was found so :code:`zurich_switzerland.mbtiles` was downloaded.
* A :code:`config.json` file was automatically created.
* This `basic preview <https://github.com/openmaptiles/maptiler-basic-gl-style>`_ style is used.
* Running with :code:`--verbose` will give us information about :code:`config.json`.

Visiting :code:`http://localhost:8080` in a web browser will show us the tile server. 
There are two important sections styles and data.
 
 .. image:: ../images/tileserver.png
   :width: 900

The config file
*****************
The TileServer GL `documentation <https://tileserver.readthedocs.io/en/latest/config.html>`_ 
shows all the possible options for the :code:`config.json` file. However, running the docker command
from the output above with :code:`--verbose` will show the one used by :code:`make start-tileserver`.

.. code-block::

   docker run --rm --user=501:20 -it --name tileserver-gl -v $(pwd)/data:/data -p 8080:8080 maptiler/tileserver-gl --port 8080 --verbose

This returns a slightly longer output with the :code:`config.json` file.
 
 .. image:: ../images/config.png
   :width: 900

The :code:`config.json` file is seen below,

.. literalinclude:: ../configs/default_config.json
  :language: JSON

Here it is clear

Creating a custom style with maputnik
--------------------------------------

Bringing it all together
--------------------------------------
