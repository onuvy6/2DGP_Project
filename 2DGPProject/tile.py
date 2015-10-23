__author__ = 'dustinlee'

import json

from pico2d import *

MAP_ORIENTATION_UNKNOWN, MAP_ORIENTATION_ORTHOGONAL, MAP_ORIENTATION_HEXAGONAL = 0, 1, 4

class TileMap:
    def get_tile_image_rect(self, id):
        y = self.tile_rows - id // self.tile_cols - 1
        x = id % self.tile_cols
        return self.image_margin+x*(self.tile_width+self.image_spacing), \
               self.image_margin+y*(self.tile_height+self.image_spacing), \
               self.tile_width, self.tile_height

    def draw_to_origin(self, left, bottom, w=None, h=None):
        if w == None and h == None:
            w,h = self.map_width, self.map_height

        for y in range(h):
            for x in range(w):
                id = self.map2d[y][x]
                self.tileset_image.clip_draw_to_origin(*self.get_tile_image_rect(id), x=(x+left)*self.tile_width, y=(y+bottom)*self.tile_height)



    def clip_draw_to_origin(self, left, bottom, width, height, target_left, target_bottom, w=None, h=None):
        if w == None and h == None:
            w,h = width, height
        
        # TODO: Orientation에 맞춰서 Render하는 기능 필요
        #for y in range(h):
        #    for x in range(w):    
        for map2d in self.map2d:
            for y in reversed(range(h)):
                for x in reversed(range(w)):
                    id = map2d[bottom+y][left+x]

                    if self.map_orientation == MAP_ORIENTATION_ORTHOGONAL:
                        self.tileset_image.clip_draw_to_origin(*self.get_tile_image_rect(id), x=(x+target_left)*self.tile_width, y=(y+target_bottom)*self.tile_height),
                    elif self.map_orientation == MAP_ORIENTATION_HEXAGONAL:
                        self.tileset_image.clip_draw_to_origin(*self.get_tile_image_rect(id), x=(x+target_left)*self.tile_width + (y%2)*self.tile_width/2, y=(y+target_bottom)*self.tile_height/2),
                    else:
                        pass
                

def load_tile_map(name):
    with open(name) as f:
        data = json.load(f)

    tile_map = TileMap()

    base_tile_width = data['tilewidth']
    base_tile_height = data['tileheight']

    tileset = data['tilesets'][0]
    tileset_image_file_name = tileset['image']
    image_height = tileset['imageheight']
    image_width = tileset['imagewidth']
    image_margin = tileset['margin']
    image_spacing = tileset['spacing']
    tile_height = tileset['tileheight']
    tile_width = tileset['tilewidth']
    first_gid = tileset['firstgid']
    
    # Furthermore, you could be more defensive and refer to data.get('data', []) when starting the loop in case Instagram sends you empty JSON.
    # http://stackoverflow.com/questions/11748234/check-whether-the-json-object-property-exists-print-it-as-unicode-decoded
    if tileset.get('tiles') == None:
        num_tiles = 0
    else:
        num_tiles = len(tileset['tiles'])

    #tile_cols = (image_width - 1) // (tile_width + 1)
    #tile_rows = (image_height - 1) // (tile_height + 1)
    tile_cols = (image_width) // (tile_width)
    tile_rows = (image_height) // (tile_height)

    tile_map.map2d = []

    layers = data['layers']
    for layer in layers:
        #print(layer['type'])
        #print(data['renderorder'])
        map_height = layer['height']
        map_width = layer['width']
        tile_data = layer['data']
        render_order = data['renderorder']
        map_orientation = data['orientation']

        '''
        h = 4
        w = 8
        tile_data = [i for i in range(h*w)]
        '''

        map2d = []

        if render_order == 'right-up':
            for i in range(map_height):
                line = [x - first_gid for x in tile_data[i*map_width:i*map_width+map_width]]
                map2d.append(line)
        else:
            for i in reversed(range(map_height)):
                line = [x - first_gid for x in tile_data[i*map_width:i*map_width+map_width]]
                map2d.append(line)

        tile_map.map2d.append(map2d)

    tile_map.tileset_image = load_image(tileset_image_file_name)
    tile_map.image_margin = image_margin
    tile_map.image_spacing = image_spacing
    tile_map.map_width = map_width
    tile_map.map_height = map_height
    tile_map.tile_width = tile_width
    tile_map.tile_height = tile_height
    tile_map.tile_rows = tile_rows
    tile_map.tile_cols = tile_cols
    map_orientation_state = {
        'orthogonal' : MAP_ORIENTATION_ORTHOGONAL,
        'hexagonal' : MAP_ORIENTATION_HEXAGONAL
    }
    tile_map.map_orientation = map_orientation_state[map_orientation];

    return tile_map