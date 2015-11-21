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

        if tileset is None:
            return (0, 0, 0, 0)

        id = gid - tileset.firstgid
        x = id % tileset.tilecols
        y = tileset.tilerows - (id // tileset.tilecols) - 1

        return (tileset.margin + x * (tileset.tilewidth + tileset.spacing),  \
                tileset.margin + y * (tileset.tileheight + tileset.spacing), \
                tileset.tilewidth,                                           \
                tileset.tileheight)


    def draw(self, w, h):
        draw_layer_type = {
            'tilelayer'     : self.draw_tile_layer,
            'objectgroup'   : self.draw_object_layer,
            'imagelayer'    : self.draw_image_layer
        }
        for layer in self.layers:
            draw_layer_type[layer.type](w, h, layer)


    def draw_tile_layer(self, w, h, layer):
        if self.orientation == 'orthogonal':
            pass

        elif self.orientation == 'isometric':
            pass

        elif self.orientation == 'hexagonal':
            for y in reversed(range(layer.height)):
                for x in reversed(range(layer.width)):
                    gid = layer.data[y][x]
                    if gid is 0:
                        continue
                    tileset = self.to_tileset(gid)
                    if tileset is not None:
                        _x = (x) * tileset.tilewidth + (y % 2) * (tileset.tilewidth // 2)
                        _y = (y) * (tileset.tileheight // 2)
                        tileset.image.clip_draw_to_origin(*self.to_rect(gid), x=((w - self.mapwidth) // 2) + _x, y=_y)
        else:
            pass


    def draw_object_layer(self, w, h, layer):
        for object in layer.objects:
            gid = object.gid
            tileset = self.to_tileset(gid)
            if tileset is not None:
                _x = object.x
                _y = ((self.height - 1) * (tileset.tileheight // 2)) - object.y
                tileset.image.clip_draw_to_origin(*self.to_rect(gid), x=((w - self.mapwidth) // 2) + _x, y=_y)


    def draw_image_layer(self, w, h, layer):
        pass

