# Tiled map options
tilesource='maptiler'
tile_sources={
    'opentopomap': {
        'source': ['https://a.tile.opentopomap.org/{zoom}/{x}/{y}.png',
                    'https://b.tile.opentopomap.org/{zoom}/{x}/{y}.png',
                    'https://c.tile.opentopomap.org/{zoom}/{x}/{y}.png'],
        'max_download_workers': 2,
        'max_tile_zoom': 17,
        'license': 'map data: © OpenStreetMap contributors, SRTM | map style: © OpenTopoMap.org (CC-BY-SA)'},
    'maptiler': {
        'source': ['https://api.maptiler.com/maps/streets/{zoom}/{x}/{y}.png?key='],
        'max_download_workers': 20,
        'max_tile_zoom': 20,
        'license': '© MapTiler © OpenStreetMap contributors'
        }
    }