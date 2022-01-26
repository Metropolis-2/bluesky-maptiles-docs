# %%
from ipyleaflet import Map, TileLayer, LocalTileLayer, basemaps

m = Map(center=(48.2082, 16.3738), zoom=12)
m.add_layer(LocalTileLayer(path='m2/{z}/{x}/{y}.png'))

# # create empty basemap
# p = Map(center=(48.2082, 16.3738), zoom=11)
# p.add_layer(TileLayer(url='http://localhost:8080/styles/m2/{z}/{x}/{y}.png',
#                         attribution='Map data (c) <a href=’https://openstreetmap.org’>OpenStreetMap</a> contributors (c) City of Vienna'))
# # remove basemap
m.remove_layer(m.layers[0])
# %%
# p.save('my_map.html', title='My Map')