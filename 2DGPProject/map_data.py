import collision
import pico2d_extension
import game_framework


class MapData:

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


    def to_tileset(self, gid):
        id = gid
        for tileset in self.tilesets:
            if tileset.tilecount < id:
                id -= tileset.tilecount
                continue
            return tileset
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


    def to_object_rect(self, object):
        gid = object.gid
        tileset = self.to_tileset(gid)
        
        object_y = game_framework.height - object.y

        return object.x - (tileset.tilewidth // 2), object_y - (tileset.tileheight // 2), \
               object.x + (tileset.tilewidth // 2), object_y + (tileset.tileheight // 2)


    def update(self):
        pass

    
    def get_hexagon_index_from_point(self, x, y):

        _y = (y) // (self.tileheight // 2)
        
        for _x in range(self.width):
            hx = _x * self.tilewidth + ( (_y+1) % 2 ) * (self.tilewidth // 2)
            hy = _y * (self.tileheight // 2)
            if collision.point_in_rect(x,y,hx,hy,self.tilewidth,self.tileheight):
                return (int(_x), int(_y))
        
        return (-1, -1)


    def get_hexagon_point_from_point(self, x, y):
        
        _y = (y) // (self.tileheight // 2)
        
        for _x in range(self.width):
            hx = _x * self.tilewidth + ( (_y+1) % 2 ) * (self.tilewidth // 2)
            hy = _y * (self.tileheight // 2)
            if collision.point_in_rect(x,y,hx,hy,self.tilewidth,self.tileheight):
                return (hx, hy)
        
        return (-1, -1)
        

    def draw(self):
        draw_layer_type = {
            'tilelayer'     : self.draw_tile_layer,
            'objectgroup'   : self.draw_object_layer,
            'imagelayer'    : self.draw_image_layer
        }
        for layer in self.layers:
            draw_layer_type[layer.type](layer)
        
        # DO NOT USE
        #self.draw_grid()


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
                    tileset = self.to_tileset(gid)
                    if tileset is not None:
                        _x = (x) * tileset.tilewidth + ( (y + 1) % 2) * (tileset.tilewidth // 2)
                        _y = (y) * (tileset.tileheight // 2)
                        tileset.image.clip_draw(*self.to_rect(gid), x=((game_framework.width - self.mapwidth) // 2) + _x, y=_y)   
        else:
            pass


    def draw_object_layer(self, layer):
        pico2d_extension.set_color(255, 0, 0)
        for object in layer.objects:
            gid = object.gid
            tileset = self.to_tileset(gid)
            if tileset is not None:
                _x = object.x
                _y = game_framework.height - object.y
                tileset.image.clip_draw(*self.to_rect(gid), x=((game_framework.width - self.mapwidth) // 2) + _x, y=_y)
                pico2d_extension.draw_rectangle(_x - tileset.tilewidth // 2, _y - tileset.tileheight // 2, _x + tileset.tilewidth // 2, _y + tileset.tileheight // 2)


    def draw_image_layer(self, w, h, layer):
        pass


    def draw_hexagon(self,x,y):
        pico2d_extension.set_color(127,127,127)
        pico2d_extension.draw_hexagon(x, y, self.tilewidth // 2)


    def draw_hexagon_on_point(self,x,y):
        point = self.get_hexagon_point_from_point(x,y)
        self.draw_hexagon(*point)
