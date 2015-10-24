import json

from pico2d import *


class Object:
    def __init__(self):
        self.id = 0
        self.width = 0
        self.height = 0
        self.name = ''
        self.type = ''
        self.properties = []
        self.visible = True
        self.x = 0
        self.y = 0
        self.rotation = 0.0
        self.gid = 0
        pass
           
         
class Layer:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.name = ''
        self.type = ''
        self.visible = True
        self.x = 0
        self.y = 0
        self.data = []
        self.properties = []
        self.opacity = 0.0
        self.draworder = ''
        self.objects = []
        pass


class TileSet:
    def __init__(self):
        self.first_gid = 0
        self.image = None
        self.name = ''
        self.tile_width = 0
        self.tile_height = 0
        self.image_width = 0
        self.image_height = 0
        self.properties = []
        self.margin = 0
        self.spacing = 0
        self.tile_properties = []
        self.terrains = []
        self.tiles = []
        self.tile_count = 0
        
        # +
        self.tile_cols = 0
        self.tile_rows = 0
        pass

class Tile:
    pass


class Terrain:
    pass


class TileMap:
    def get_tile_image_rect(self, gid):

        for tileset in self.tilesets:
            if tileset.tile_count < gid:
                continue

            y = tileset.tile_rows - (gid-tileset.first_gid) // tileset.tile_cols - 1
            x = (gid-tileset.first_gid) % tileset.tile_cols;
        
            return tileset.margin + x * (tileset.tile_width + tileset.spacing), \
                   tileset.margin + y * (tileset.tile_height + tileset.spacing), \
                   tileset.tile_width, tileset.tile_height
        #
        return -1, -1, -1, -1

    def get_tileset_from_gid(self, gid):
        for tileset in self.tilesets:
            if tileset.tile_count < gid:
                continue

            return tileset

        return None


    def draw_all_layer(self, target_left, target_bottom):
        draw_layer_type = {
            'tilelayer'     : self.draw_tile_layer  ,
            'objectgroup'   : self.draw_object_layer,
            'imagelayer'    : self.draw_image_layer
        }
        for layer in self.layers:
            draw_layer_type[layer.type](layer)
    
    
    def draw_tile_layer(self, layer):
        if self.map_orientation == 'orthogonal':
            for y in range(layer.width):
                for x in range(layer.height):
                    id = layer.data[y][x]
                    tileset = self.get_tileset_from_gid(id)
                    tileset.image.clip_draw_to_origin(*self.get_tile_image_rect(id), x=(x)*tileset.tile_width, y=(y)*tileset.tile_height)
        elif self.map_orientation == 'isometric':
            pass
        elif self.map_orientation == 'hexagonal':
            # TODO: Render-Order에 맞게 동작하도록 수정 필요.
             for y in reversed(range(layer.width)):
                for x in reversed(range(layer.height)):
                    id = layer.data[y][x]
                    tileset = self.get_tileset_from_gid(id)
                    tileset.image.clip_draw_to_origin(*self.get_tile_image_rect(id), x=(x)*tileset.tile_width + (y%2)*tileset.tile_width/2, y=(y)*tileset.tile_height/2)
        else:
            pass


    def draw_object_layer(self, layer):
       # if layer.name == 'Object Layer 1':
            for object in layer.objects:
                gid = object.gid
                tileset = self.get_tileset_from_gid(gid)
                tileset.image.clip_draw_to_origin(*self.get_tile_image_rect(gid), x=object.x, y = ((self.map_height-1) * self.map_tileheight/2) + self.map_tileheight - object.y)
                pass


    def draw_image_layer(self, layer):
        pass
        

def load_tile_map(name):
    with open(name) as f:
        data = json.load(f)

    
    tile_map = TileMap()    


    # Referrence    
    # https://github.com/bjorn/tiled/wiki/JSON-Map-Format

    # Map ########################################################################
    # Number of tile columns
    tile_map.map_width = data.get('width')
    # Number of tile rows
    tile_map.map_height = data.get('height')

    # Map grid width.
    tile_map.map_tilewidth = data.get('tilewidth')
    # Map grid height.
    tile_map.map_tileheight = data.get('tileheight')

    # Orthogonal, isometric, or staggered
    tile_map.map_orientation = data.get('orientation')

    # Hex-formatted color (#RRGGBB) (Optional)
    tile_map.map_backgroundcolor = data.get('backgroundcolor')

    # Rendering direction (orthogonal maps only)
    tile_map.map_renderorder = data.get('renderorder')

    # String key-value pairs
    tile_map.map_properties = data.get('properties');

    # Auto-increments for each placed object
    tile_map.map_nextobjectid = data.get('nextobjectid')

    # Layer ######################################################################
    tile_map.layers = []
    for _layer in data.get('layers'):

        layer = Layer()

        # Column count. Same as map width in Tiled Qt.
        layer.width = _layer.get('width')
        # Row count. Same as map height in Tiled Qt.
        layer.height = _layer.get('height')

        # Name assigned to this layer
        layer.name = _layer.get('name')

        # "tilelayer", "objectgroup", or "imagelayer"
        layer.type = _layer.get('type')

        # Whether layer is shown or hidden in editor
        layer.visible = _layer.get('visible')

        # Horizontal layer offset. Always 0 in Tiled Qt.
        layer.x = _layer.get('x')
        # Vertical layer offset. Always 0 in Tiled Qt.
        layer.y = _layer.get('y')

        # Array of GIDs. tilelayer only.
        layer_data = _layer.get('data')
        if layer_data != None:
            # TODO: Render-Order에 맞게 동작하도록 수정 필요.
            if tile_map.map_renderorder == 'right-up':
                for i in range(layer.height):
                    line = [x for x in layer_data[i * layer.width : i * layer.width + layer.width]]
                    layer.data.append(line)
            else:
                for i in reversed(range(layer.height)):
                    line = [x for x in layer_data[i * layer.width : i * layer.width + layer.width]]
                    layer.data.append(line)
                        

        # Array of Objects. objectgroup only.
        layer_objects = _layer.get('objects')

        if layer_objects != None:
            
            for _object in layer_objects:
                object = Object()
                # Incremental id - unique across all objects
                object.id = _object.get('id')

                # Width in pixels. Ignored if using a gid.
                object.width = _object.get('width')
                # Height in pixels. Ignored if using a gid.
                object.height = _object.get('height')

                # String assigned to name field in editor
                object.name = _object.get('name')

                # String assigned to type field in editor
                object.type = _object.get('type')

                # String key-value pairs
                object.properties = _object.get('properties')

                # Whether object is shown in editor.
                object.visible = _object.get('visible')

                # x coordinate in pixels
                object.x = _object.get('x')
                # y coordinate in pixels
                object.y = _object.get('y')

                # Angle in degrees clockwise
                object.rotaion = _object.get('rotation')

                # GID, only if object comes from a Tilemap
                object.gid = _object.get('gid')

                layer.objects.append(object)

        # string key-value pairs.
        layer.properties = _layer.get('properties')

        # Value between 0 and 1
        layer.opacity = _layer.get('opacity')

        # "topdown" (default) or "index". objectgroup only.
        layer.draworder = _layer.get('draworder')

        tile_map.layers.append(layer)

    tile_map.tilesets = []
    # Tileset ######################################################################
    map_tilesets = data.get('tilesets')
    if map_tilesets != None:
        for _tileset in map_tilesets:

            tileset = TileSet()

            # GID corresponding to the first tile in the set
            tileset.first_gid = _tileset.get('firstgid')

            # Image used for tiles in this set
            image = _tileset.get('image')

            tileset.image = load_image(image)

            # Name given to this tileset
            tileset.name = _tileset.get('name')

            # Maximum width of tiles in this set
            tileset.tile_width = _tileset.get('tilewidth')
            # Maximum height of tiles in this set
            tileset.tile_height = _tileset.get('tileheight')

            # Width of source image in pixels
            tileset.image_width = _tileset.get('imagewidth')
            # Height of source image in pixels
            tileset.image_height = _tileset.get('imageheight')

            tileset.tile_cols = tileset.image_width // tileset.tile_width
            tileset.tile_rows = tileset.image_height // tileset.tile_height

            tileset.tile_count = _tileset.get('tilecount')

            # String key-value pairs
            tileset.properties = _tileset.get('properties')

            # Buffer between image edge and first tile (pixels)
            tileset.margin = _tileset.get('margin')
            # Spacing between adjacent tiles in image (pixels)
            tileset.spacing = _tileset.get('spacing')

            # Per-tile properties, indexed by gid as string
            tileset.tile_properties = _tileset.get('tileproperties')

            # Gid-indexed Tiles (optional)
            tilesets_tiles = _tileset.get('tiles')
            if tilesets_tiles != None:
                for _tile in tilesets_tiles:
                    tile = Tile()
                    # index of terrain for each corner of tile
                    tile.terrain = _tile.get('terrain')

                    tileset.tiles.append(tile)

            # Array of Terrains (optional)
            tilesets_terrains = _tileset.get('terrain')    
            if tilesets_terrains != None:
                for _terrain in tilesets_terrains:
                    terrain = Terrain()
                    # Name of terrain
                    terrain.name = _terrain.get('name')

                    # Local ID of tile representing terrain
                    terrain.tile = _terrain.get('tile')

                    tileset.terrains.append(terrain)

            tile_map.tilesets.append(tileset)

    return tile_map