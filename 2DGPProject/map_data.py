import collision
import pico2d
import pico2d_extension
import game_framework
import random


class MapData:

    disappear_wait_min_time = 1
    disappear_wait_max_time = 3
    disappear_frame_time = 0.01

    def __init__(self):
        # Number of tile columns
        self.width = 0
        # Number of tile rows
        self.height = 0

        # Map grid width.
        self.tilewidth = 0
        # Map grid height.
        self.tileheight = 0

        self.mapwidth = 0
        self.mapheight = 0

        self.mapoffsetx = 0
        self.mapoffsety = 0

        # Orthogonal, isometric, or staggered
        self.orientation = ''

        # Array of Layers
        self.layers = []
   
        # Array of Tilesets
        self.tilesets = []

        # Hex-formatted color (#RRGGBB) (Optional)
        self.backgroundcolor = ''
        # Rendering direction (orthogonal maps only)
        self.renderorder = ''

        # Auto-increments for each placed object
        self.nextobjectid = 0

        self.disappear_tile_exist = True
    
        self.disappear_tile_col = 0
        self.disappear_tile_row = 0

        self.disappear_height = 0
        self.disappear_tile_opacify = 1.0

        self.disappear_tile_wait_time = random.randint(MapData.disappear_wait_min_time, MapData.disappear_wait_max_time) * 0.1
        self.disappear_tile_remain_time = MapData.disappear_frame_time

        self.draw_layer_type = {
            'tilelayer'     : self.draw_tile_layer,
            'objectgroup'   : self.draw_object_layer,
            'imagelayer'    : self.draw_image_layer
        }

        self.tile_layer = None
        self.collision_layer = None
        self.trigger_layer = None


    def to_tileset(self, gid):
        id = gid
        for tileset in self.tilesets:
            if tileset.tilecount < id:
                id -= tileset.tilecount
                continue
            return tileset
        return None


    def to_trigger(self, name):
        for object in self.trigger_layer.objects:
            if object.name == name:
                return object
        return None


    def to_rect(self, gid):
        tileset = self.to_tileset(gid)

        if tileset == None:
            return (0, 0, 0, 0)

        id = gid - tileset.firstgid
        x = id % tileset.tilecols
        y = tileset.tilerows - (id // tileset.tilecols) - 1

        return (tileset.margin + x * (tileset.tilewidth + tileset.spacing),  \
                tileset.margin + y * (tileset.tileheight + tileset.spacing), \
                tileset.tilewidth,                                           \
                tileset.tileheight)


    def is_tile_on_object(self,x,y):
        for object in self.collision_layer.objects:
            object_rect = self.to_object_rect(object)
            
            tile_rect = (
                self.mapoffsetx + x * self.tilewidth + ( (y+1) % 2 ) * (self.tilewidth // 2),
                self.mapoffsety + (y) * (self.tileheight // 2),
                self.mapoffsetx + (x+1) * self.tilewidth + ( (y+1) % 2 ) * (self.tilewidth // 2),
                self.mapoffsety + (y+1) * (self.tileheight // 2),
                )

            if collision.rect_in_rect(*(object_rect+tile_rect)):
                return True

        return False


    def get_disappear_next_tile(self):
        for y in range(self.disappear_tile_col, self.tile_layer.height):
                for x in range(0, self.tile_layer.width):
                    if self.tile_layer.data[y][x] != 0:

                        # 해당 Tile 위에 Object가 있다면 처리하지 않습니다.
                        if self.is_tile_on_object(x,y):
                            continue
                                 
                        self.disappear_tile_col = y
                        self.disappear_tile_row = x
                        return True
        return False          


    def to_tileset_object_rect(self, object):
        object_x = self.mapoffsetx + object.x
        object_y = self.mapoffsety + self.mapheight - object.y

        return object_x, object_y, \
               object_x + object.width, object_y + object.height


    def to_object_rect(self, object):

        object_x = self.mapoffsetx + object.x
        object_y = self.mapoffsety + self.mapheight - object.y - object.height

        return object_x, object_y, \
               object_x + object.width, object_y + object.height


    def update(self, frame_time):
        if self.disappear_tile_exist:

            self.disappear_tile_wait_time -= frame_time
            if self.disappear_tile_wait_time < 0:

                self.disappear_tile_remain_time -= frame_time
                if self.disappear_tile_remain_time < 0:

                    self.disappear_tile_remain_time = MapData.disappear_frame_time

                    self.disappear_height -= 1
                    self.disappear_tile_opacify -= 0.1

                    if self.disappear_tile_opacify <= 0.0:
                        self.disappear_tile_opacify = 1.0
                        self.disappear_height = 0

                        self.tile_layer.data[self.disappear_tile_col][self.disappear_tile_row] = 0
                        self.disappear_tile_wait_time = random.randint(MapData.disappear_wait_min_time, MapData.disappear_wait_max_time) * 0.1
                               
                        self.disappear_tile_exist = self.get_disappear_next_tile()
            
    
    def get_hexagon_index_from_point(self, x, y):

        _y = (y - self.mapoffsety) // (self.tileheight // 2)
        
        for _x in range(self.width):
            hx = self.mapoffsetx + _x * self.tilewidth + ( (_y+1) % 2 ) * (self.tilewidth // 2)
            hy = self.mapoffsety + _y * (self.tileheight // 2)
            if collision.point_in_rect(x,y,hx,hy,self.tilewidth,self.tileheight):
                return (int(_x), int(_y))
        
        return (-1, -1)


    def get_hexagon_point_from_point(self, x, y):
        
        _y = (y - self.mapoffsety) // (self.tileheight // 2)
        
        for _x in range(self.width):
            hx = self.mapoffsetx + _x * self.tilewidth + ( (_y+1) % 2 ) * (self.tilewidth // 2)
            hy = self.mapoffsety + _y * (self.tileheight // 2)
            if collision.point_in_rect(x,y,hx,hy,self.tilewidth,self.tileheight):
                return (hx, hy)
        
        return (-1, -1)
        

    def draw_ground(self):
        self.draw_layer_type[self.tile_layer.type](self.tile_layer)


    def draw_object(self):
        for layer in self.layers:
            if layer.type != 'tilelayer':
                self.draw_layer_type[layer.type](layer)


    def draw_tile_layer(self, layer):
        if self.orientation == 'orthogonal':
            pass

        elif self.orientation == 'isometric':
            pass

        elif self.orientation == 'hexagonal':
            for y in reversed(range(layer.height)):
                for x in (range(layer.width)):
        
                    gid = layer.data[y][x]
                    if gid is 0:
                        continue

                    disappear = False
                    if x == self.disappear_tile_row and y == self.disappear_tile_col:
                        disappear = True

                    tileset = self.to_tileset(gid)
                    if tileset is not None:
                        if disappear:
                            tileset.image.opacify(self.disappear_tile_opacify)

                        _x = self.mapoffsetx + (x) * tileset.tilewidth + ( (y + 1) % 2) * (tileset.tilewidth // 2)
                        _y = self.mapoffsety + (y) * (tileset.tileheight // 2)

                        if disappear:
                            _y += self.disappear_height

                        tileset.image.clip_draw(*self.to_rect(gid), x=_x, y=_y)

                        if disappear:
                            tileset.image.opacify(1.0)

        else:
            pass


    def draw_object_layer(self, layer):
        if layer.name == 'Collision Layer' or \
            layer.name == 'Trigger Layer':
            pico2d_extension.set_color(127, 127, 127)
            for object in layer.objects:
                pico2d_extension.draw_rectangle(*self.to_object_rect(object))
        else:
            pico2d_extension.set_color(255, 255, 0)
            for object in layer.objects:
                if object.visible:
                    gid = object.gid
                    tileset = self.to_tileset(gid)
                    if tileset is not None:
                        rect = self.to_tileset_object_rect(object)
                        tileset.image.clip_draw_to_origin(*self.to_rect(gid), x=rect[0], y=rect[1])
                        if game_framework.debug:
                            pico2d_extension.draw_rectangle(*rect)


    def draw_image_layer(self, w, h, layer):
        pass


    def draw_hexagon(self,x,y):
        pico2d_extension.set_color(127,127,127)
        pico2d_extension.draw_hexagon(x, y, self.tilewidth // 2)


    def draw_hexagon_on_point(self,x,y):
        point = self.get_hexagon_point_from_point(x,y)
        self.draw_hexagon(*point)
