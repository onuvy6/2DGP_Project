
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
    def __init__(self):
        self.viewRect = False

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
            # TODO: Render-Order�� �°� �����ϵ��� ���� �ʿ�.
             for y in reversed(range(layer.width)):
                for x in reversed(range(layer.height)):
                    id = layer.data[y][x]
                    tileset = self.get_tileset_from_gid(id)
                    rx = (x)*tileset.tile_width + (y%2)*tileset.tile_width/2;
                    ry = (y)*tileset.tile_height/2
                    tileset.image.clip_draw_to_origin(*self.get_tile_image_rect(id), x=rx, y=ry)
                    
                    if self.viewRect:
                        if id != 0:
                            pico2d.draw_rectangle(rx , ry , rx + self.map_tilewidth, ry + self.map_tileheight)
        else:
            pass


    def draw_object_layer(self, layer):
        for object in layer.objects:
            gid = object.gid
            tileset = self.get_tileset_from_gid(gid)
            rx = object.x
            ry = ((self.map_height-1) * self.map_tileheight/2) + self.map_tileheight - object.y
            tileset.image.clip_draw_to_origin(*self.get_tile_image_rect(gid), x=rx, y = ry)
            
            if self.viewRect:
                self.drawRect(rx , ry , rx + self.map_tilewidth, ry + self.map_tileheight)
            pass


    def draw_image_layer(self, layer):
        pass


    def drawRect(self, x1, y1, x2, y2):
        SDL_SetRenderDrawColor(pico2d.renderer, 0, 0, 255, 255)
        rect = SDL_Rect(int(x1),int(-y2+pico2d.canvas_height-1),int(x2-x1+1),int(y2-y1+1))
        SDL_RenderDrawRect(pico2d.renderer, rect)
        