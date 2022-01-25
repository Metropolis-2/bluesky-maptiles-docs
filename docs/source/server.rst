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
shows all the possible options for the :code:`config.json` file. In this section we
will talk about the main parts that we need for Metropolis-2.

Running the docker command from the output above with :code:`--verbose` will show the one used by :code:`make start-tileserver`.

.. code-block::

   docker run --rm --user=501:20 -it --name tileserver-gl -v $(pwd)/data:/data -p 8080:8080 maptiler/tileserver-gl --port 8080 --verbose

This returns a slightly longer output with the :code:`config.json` file.
 
 .. image:: ../images/config.png
   :width: 900

The :code:`config.json` file is as follows.

.. literalinclude:: ../configs/default_config.json
  :language: JSON

There important parts of the config file are (1) **options**, (2) **styles**, (3) **data**.

For this tutorial we will only work with the parts shown in the default :code:`config.json`. 
Now that we have all the data the most difficult part is pretty much done. The trick now
is to get the paths right inside **options**. In the current config, the root directory is somewhere inside our docker shell.

If we open a new terminal and enter the docker shell, we can navigate to the root directory.

 .. image:: ../images/docker_root.png
   :width: 900

The other paths (:code:`fonts`, :code:`styles`, and :code:`mbtiles`) are dependent on the :code:`root` path. 
For example to navigate to :code:`fonts` we would have to visit :code:`/app/node_modules/tileserver-gl-styles/fonts` 
You can see this directory in the image above. It is the sames for :code:`styles`. However, if you take a look at the image above
you won't find the :code:`mbtiles` path because the path starts with a forward slash (:code:`/`). In this case it means that we
need to look inside the :code:`/data/` directory of the docker shell.

 .. image:: ../images/docker_root_data.png
   :width: 900

This :code:`data` directory inside the docker shell is actually just a copy of :code:`openmaptiles/data`.

In the future this is where we will place our vector tiles, style schema, and fonts 
(you can also put some sprites there but we will not be doing that in this tutorial).

About fonts
*****************

If you visit the :code:`/app/node_modules/tileserver-gl-styles/fonts` directory in the docker shell you 
will see a :code:`Noto Sans Regular` font directory with a bunch of :code:`pbf` files.
These are the default fonts of the server. If a custom style references a non existent font,
the server will use the default font. For most of my cases, the default is fine.

However, to use other fonts we can look at at the OpenMapTiles `font <https://github.com/openmaptiles/fonts>`_ 
repository and either:

* package the fonts.
* set :code:`"glyphs": "http://fonts.openmaptiles.org/{fontstack}/{range}.pbf"` in the style schema.
  
Since we are attempting to do everyhting locally, we will package the fonts following 
these `instructions <https://github.com/openmaptiles/fonts#package-the-fonts>`_.

See TileServer GL documentation for more information.

About styles
*****************

If we look again at the :code:`config.json` file we see the :code:`basic-preview` style located at
:code:`/app/node_modules/tileserver-gl-styles/styles/basic-preview/style.json`. It also
has some information about the bounding box of the tiles (not required but nice).

The :code:`style.json` is almost a complete copy of of `this <https://github.com/openmaptiles/maptiler-basic-gl-style/blob/master/style.json>`_.
The only difference are the paths to the vector tiles and glyphs. The online version is linking to
the MapTiler server, while the one in the docker shell is linking to a local path. You can actually
use any path (local or remote), however some paths may require an api key (mapbox or MapTiler).
Below you can see just the top of the :code:`style.json` file in the docker shell.

.. literalinclude:: ../configs/basic.json
  :language: JSON

Under :code:`sources` you can see that the OpenMapTiles vector tiles are linked to the local tiles :code:`v3`.
Looking at the :code:`config.json` above we can see that those are the :code:`zurich_switzerland.mbtiles`.

The :code:`glyphs` path is set to :code:`{fontstack}/{range}.pbf` which means that the font will depend on whatever
the layer (more on this later) uses. The basic preview style only uses the :code:`Noto Sans Regular` font which comes packaged with
OpenMapTiles.

About sprites
*****************
The Metropolis-2 tiles will not be using sprites but it is worth briefly mentioning them.

The `dark matter style <https://github.com/openmaptiles/dark-matter-gl-style/blob/master/style.json>`_ provides an example
path to sprites.

.. code-block::

   "sprite": "https://openmaptiles.github.io/dark-matter-gl-style/sprite"

When a style contains a reference to a sprite it will try to look in this path. The documentation for sprites says
that the following files be present, :code:`sprite.json`, :code:`sprite.png`, :code:`sprite@2x.json`, :code:`sprite@2x.json`.
If you add these file extensions to the sprite path of the dark matter style you can see how they look.

* `<https://openmaptiles.github.io/dark-matter-gl-style/sprite.json>`_
* `<https://openmaptiles.github.io/dark-matter-gl-style/sprite.png>`_
* `<https://openmaptiles.github.io/dark-matter-gl-style/sprite@2x.json>`_
* `<https://openmaptiles.github.io/dark-matter-gl-style/sprite@2x.png>`_

As always you can also reference them locally.

Creating the Metropolis-2 style
---------------------------------
There is already a nice tutorial on how to use `maputnik <https://github.com/maputnik/editor/wiki>`_ for custom styles.
It has an online version that can sync with your local :code:`style.json`. The benefit is that if you just create
a vanilla :code:`mbtiles` file with OpenMapTiles then you can design your style without adding your local :code:`mbtiles`
to maputnik becuase maputnik can serve tiles from MapTiler without an api key. However, when serving with TileServer GL
you need to replace the tile source, sprites, and glyphs paths with a local path or get a MapTiler api key.

.. note::

   `OpenMapTiles <https://openmaptiles.org/styles/>`_ provides several open source styles that are a good starting point for beginners.
   These can be loaded directly into maputnik.

   You can use any tiles in maputnik as long as they adhere to the :code:`mbtiles` convention. 
   I alternate between mapbox and MapTiler. However a MapTiler style is not compatible with a mapbox style
   even if they both use OpenStreetMap as they have different layers.

For Metropolis-2, it is not possible to design the style this way because it does not use the same layer schema
as OpenMapTiles or Maptiler. Since, we modified the data considerably we need to add them as a source.

Adding our local tiles to maputnik
***********************************

There is no way to directly add :code:`m2.mbtiles` as a source to maputnik. Among other things, it accepts :code:`GeoJSON` and :code:`TileJSON`
but not :code:`mbtiles`. Luckily, TileServer GL can serve an :code:`mbtiles` file as a TileJSON. If you look at the image
of the TileServer GL homepage above you can see that there is a TileJSON button. If you click that and get the url it looks like this:

`<http://localhost:8080/data/v3.json>`_

So ideally, we can now add this url to maputnik and see our data. However, to do this we need the local `maputnik CLI <https://github.com/maputnik/editor/wiki/Maputnik-CLI>`_
because the online editer only works with Hypertext Transfer Protocol Secure (:code:`https`). So unless you serve the tiles to a public url
you will not be able to see the data.

Serve a TileJSON
^^^^^^^^^^^^^^^^^^

Now we are ready to serve the Metropolis-2 tiles to start designing our style.

So at this point we can make changes to :code:`openmaptiles/data` before starting the server.

Step 1
"""""""
Place :code:`m2.mbtiles` in :code:`openmaptiles/data`

Step 2
"""""""
Place the following :code:`config.json` in :code:`openmaptiles/data`

.. literalinclude:: ../configs/server.json
  :language: JSON

Note how that by setting :code:`"root": ""` the root directory will be inside :code:`/data/` in the docker container.

Step 3
""""""""
Make a directory called :code:`fonts` in :code:`openmaptiles/data` and copy the fonts created with OpenMaptiles fonts.

Step 4
""""""""
Make a directory called :code:`styles` in :code:`openmaptiles/data`. It can remain empty for the time being.

At this point your :code:`openmaptiles/data` directory should look like this:

.. image:: ../images/styleserver.png
   :width: 900

Step 5
""""""""
Start the server by running :code:`make start-tileserver` in :code:`openmaptiles`. 
Now visit `<http://localhost:8080>`_ and you should only see your data. If you click "inspect" you should see
something like this 

.. image:: ../images/data.png
   :width: 900

Note the 4 available layers in the top right and how you can hover over the geometry to get more information.

Step 6
""""""""
In the home page of the server you can now find the link to the TileJSON:

`<http://localhost:8080/data/v3.json>`_

Note how it is an :code:`http` url.

Add :code:`http` url as a source in maputnik
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now that the server is running with the Metropolis-2 tiles, we can add it as a source to maputnik.
The Metropolis-2 style will be inspired by the dark matter style from OpenMaptiles.

Step 1
"""""""
Download the dark matter :code:`style.json` from github

`<https://github.com/openmaptiles/dark-matter-gl-style/blob/master/style.json>`_

then place it inside :code:`openmaptiles/data/styles`.

Step 2
"""""""
Change line 2 to :code:`"name": "m2",`

Step 3
""""""""
Assuming you have installed the Maputnik-CLI correctly run :code:`maputnik --watch --file style.json`
from :code:`openmaptiles/data/styles`. This will make sure any changes made in maputnik are saved
to your file. 

If it went well, you can now visit

`<http://localhost:8000>`_

and you will see the maputnik editor with the dark matter style.

Step 4
""""""""
Click **Data Sources** at the top of the page and add the the source in the pop-up window.

.. image:: ../images/sources.png
   :width: 900

If you click **View** at the top and select *Inspect* and then navigate to Vienna you will see our Data
overlayed with the MapTiler data. 

.. image:: ../images/maputnik.png
   :width: 900

.. note::

   We could already remove the openmaptiles source. However, because all the style layers reference it, removing it would
   give us a big error and make it difficult to style.

   For the time being it is better to modify the style layers.

Make style layers
^^^^^^^^^^^^^^^^^^^^^^^^^^
Now we can start making our styling layers which will reference the :code:`mbtiles` layers

* **airspace_border**
* **buildings**
* **geofences**
* **streets**

There are already some good tutorials for styling with maputnik on their github so I will not spend
too much time describing it.

Here I will go over the main general steps for the Metropolis-2 style.

Streets layer
""""""""""""""""

For this layer I just slightly modified two style layers

* :code:`highway_major_casing`
* :code:`highway_major_casing`

This involved:

#. changing the source to :code:`m2` and the source layer to :code:`streets`.
#. removing the class filter.
#. Makinf the backgrounda little lighter.
#. Change the minimum zoom to 9.

I then deleted the rest of the layers. Now everything is referencing :code:`m2` so I can remove the OpenMaptiles source.

.. image:: ../images/streets.png
   :width: 900

Airspace border layer
""""""""""""""""""""""""""
The airspace border is just a simple line. The main thing is that I want it to be available at all zoom levels.

.. image:: ../images/airspace.png
   :width: 900

Geofence layer
""""""""""""""""""""""""""
This will require two style layers. One for the geometry and one for the label of the geofence.

For the geometry, all we need to do is create a fill layer add an outline color and make it available to a minimum of zoom 8.

For the label, we use the **id** property and make it available only when zoomed in to at least a zoom level of 15.

.. image:: ../images/geofences.png
   :width: 900

The font, **Open Sans Regular**,  is located at :code:`openmaptiles/data/fonts`.

Building layer
""""""""""""""""""""""""""
The building layer is pretty much the same as the geofence layer. The main difference is that the geometry and labels are only visible
at a minimum zoom level of 15.

In this case the label is called **fid**.

.. image:: ../images/buildings.png
   :width: 900

Maputnik saves the :code:`style.json` automatically so we can close a maputnik and our data tile server.

Serving the styled tiles
-------------------------------

At this point we have a working style for the :code:`m2.mbtiles` However, the :code:`config.json` and :code:`style.json` 
are still not ready for TileServer GL.

Final touches to :code:`style.json`
**************************************

After playing with the style schema in maputnik there are still some small changes needed to make sure the tile server works.

#. Ensure the name is :code:`m2`
#. Change the sources url to :code:`"url": "mbtiles://{v3}"`
#. Change the glyphs to :code:`"glyphs": "{fontstack}/{range}.pbf"`
#. Delete the :code:`sprites` entry.
#. Change the id entry to :code:`"id": "m2"`
#. Delete the metadata entry (not required)

The :code:`style.json` file ends up like this,

.. literalinclude:: ../configs/style.json
  :language: JSON

Final touches to :code:`config.json`
**************************************

Now we need to add a style entry so the tile server can use our m2 style.

This final config file looks like this,

.. literalinclude:: ../configs/config.json
  :language: JSON

