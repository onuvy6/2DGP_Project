class TileData:
    def __init__(self):
        # index of terrain for each corner of tile
        self.terrain = []


class TerrainData:
    def __init__(self):
        # Name of terrain
        self.name = ''

        # Local ID of tile representing terrain
        self.tile = 0


class TileSetData:
    def __init__(self):
        # GID corresponding to the first tile in the set
        self.firstgid = 0

        # Image used for tiles in this set
        self.image = None

        # Name given to this tileset
        self.name = ''

        # Maximum width of tiles in this set
        self.tilewidth = 0
        # Maximum height of tiles in this set
        self.tileheight = 0

        # Width of source image in pixels
        self.imagewidth = 0
        # Height of source image in pixels
        self.imageheight = 0

        self.tilecols = 0
        self.tilerows = 0

        self.tilecount = 0

        # Buffer between image edge and first tile (pixels)
        self.margin = 0
        # Spacing between adjacent tiles in image (pixels)
        self.spacing = 0

        # Per-tile properties, indexed by gid as string
        self.tileproperties = []

        # Array of Terrains (optional)
        self.terrains = []

        # Gid-indexed Tiles (optional)
        self.tiles = [];

