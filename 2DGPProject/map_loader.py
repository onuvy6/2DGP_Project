import json
import pico2d

from map_data       import *
from layer_data     import *
from object_data    import *
from tile_data      import *


def load_map(name):
    with open(name) as f:
        data = json.load(f)

        # https://github.com/bjorn/tiled/wiki/JSON-Map-Format
        map_data = MapData()

        # MAP ########################################################################
        # Number of tile columns
        map_data.width = data.get('width')
        # Number of tile rows
        map_data.height = data.get('height')

        # Map grid width.
        map_data.tilewidth = data.get('tilewidth')
        # Map grid height.
        map_data.tileheight = data.get('tileheight')

        map_data.mapwidth = map_data.width * map_data.tilewidth
        map_data.mapheight = map_data.height * map_data.tileheight

        # Orthogonal, isometric, or staggered
        map_data.orientation = data.get('orientation')
        
        # Hex-formatted color (#RRGGBB) (Optional)
        map_data.backgroundcolor = data.get('backgroundcolor')

        # Rendering direction (orthogonal maps only)
        map_data.renderorder = data.get('renderorder')

        # Auto-increments for each placed object
        map_data.nextobjectid = data.get('nextobjectid')

        # LAYER ######################################################################
        # Array of Layers
        for layer in data.get('layers'):
            layer_data = LayerData()

            # Column count. Same as map width in Tiled Qt.
            layer_data.width = layer.get('width')
            # Row count. Same as map height in Tiled Qt.
            layer_data.height = layer.get('height')
        
            # Name assigned to this layer
            layer_data.name = layer.get('name')
            # "tilelayer", "objectgroup", or "imagelayer"
            layer_data.type = layer.get('type')

            # Whether layer is shown or hidden in editor
            layer_data.visible = layer.get('type')

            # Horizontal layer offset. Always 0 in Tiled Qt.
            layer_data.x = layer.get('x')
            # Vertical layer offset. Always 0 in Tiled Qt.
            layer_data.y = layer.get('y')

            # TILE ###################################################################
            # Array of GIDs. tilelayer only.
            _data = layer.get('data')
            if _data is not None:
                if map_data.renderorder == 'right-up':
                    for i in range(layer_data.height):
                        line = [x for x in _data[i * layer_data.width : i * layer_data.width + layer_data.width]]
                        layer_data.data.append(line)
                else:
                    for i in reversed(range(layer_data.height)):
                        line = [x for x in _data[i * layer_data.width : i * layer_data.width + layer_data.width]]
                        layer_data.data.append(line)

            ##########################################################################

            # OBJECT #################################################################
            # Array of Objects. objectgroup only.
            objects = layer.get('objects')
            if objects is not None:
                for object in objects:
                    object_data = ObjectData()

                    # Incremental id - unique across all objects
                    object_data.id = object.get('id')

                    # Width in pixels. Ignored if using a gid.
                    object_data.width = object.get('width')
                    # Height in pixels. Ignored if using a gid.
                    object_data.height = object.get('height')

                    # String assigned to name field in editor
                    object_data.name = object.get('name')
                    # String assigned to type field in editor
                    object_data.type = object.get('type')

                    # Whether object is shown in editor.
                    object_data.visible = object.get('visible')

                    # x coordinate in pixels
                    object_data.x = object.get('x')
                    # y coordinate in pixels
                    object_data.y = object.get('y')

                    # Angle in degrees clockwise
                    object_data.rotation = object.get('rotation')

                    # GID, only if object comes from a Tilemap
                    object_data.gid = object.get('gid')

                    layer_data.objects.append(object_data)
            
            ##########################################################################

            # Value between 0 and 1
            layer_data.opacity = layer.get('opacity')

            # "topdown" (default) or "index". objectgroup only.
            layer_data.draworder = layer.get('draworder')

            map_data.layers.append(layer_data)

        ##############################################################################

        # TILESET ####################################################################
        # Array of Tileset
        tilesets = data.get('tilesets')
        if tilesets is not None:
            for tileset in tilesets:

                tileset_data = TileSetData()

                # GID corresponding to the first tile in the set
                tileset_data.firstgid = tileset.get('firstgid')
                
                # Width of source image in pixels
                tileset_data.imagewidth = tileset.get('imagewidth')
                # Height of source image in pixels
                tileset_data.imageheight = tileset.get('imageheight')

                # Maximum width of tiles in this set
                tileset_data.tilewidth = tileset.get('tilewidth')
                # Maximum height of tiles in this set
                tileset_data.tileheight = tileset.get('tileheight')

                tileset_data.tilecount = tileset.get('tilecount')

                # Image used for tiles in this set
                image = tileset.get('image')
                if image is not None:
                    tileset_data.image = pico2d.load_image(image)

                    tileset_data.tilecols = tileset_data.imagewidth // tileset_data.tilewidth
                    tileset_data.tilerows = tileset_data.imageheight // tileset_data.tileheight

                # Name given to this tileset
                tileset_data.name = tileset.get('name')

                # Buffer between image edge and first tile (pixels)
                tileset_data.margin = tileset.get('margin')
                # Spacing between adjacent tiles in image (pixels)
                tileset_data.spacing = tileset.get('spacing')

                # Per-tile properties, indexed by gid as string
                tileset_data.tileproperties = tileset.get('tileproperties')

                # TERRAIN ############################################################
                # Array of Terrains (optional)
                terrains = tileset.get('terrain')
                if terrains is not None:
                    for terrain in terrains:
                        terrain_data = TerrainData()

                        # Name of terrain
                        terrain_data.name = terrain.get('name')

                        # Local ID of tile representing terrain
                        terrain_data.tile = terrain.get('tile')

                        tileset_data.terrains.append(terrain_data)

                ######################################################################

                # TILE ###############################################################
                # Gid-indexed Tiles (optional)
                tiles = tileset.get('tiles');
                if tiles is not None:
                    for i in range(tileset_data.tilecount):
                        tile_data = TileData()

                        # index of terrain for each corner of tile
                        #tile_data.terrain = tile.get('terrain')
                        
                        tileset_data.tiles.append(tile_data)

                ######################################################################
               
                map_data.tilesets.append(tileset_data)

        ##############################################################################

        return map_data