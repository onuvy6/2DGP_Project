class LayerData:
    def __init__(self):
        # Column count. Same as map width in Tiled Qt.
        self.width = 0
        # Row count. Same as map height in Tiled Qt.
        self.height = 0
        
        # Name assigned to this layer
        self.name = ''
        # "tilelayer", "objectgroup", or "imagelayer"
        self.type = ''

        # Whether layer is shown or hidden in editor
        self.visible = True

        # Horizontal layer offset. Always 0 in Tiled Qt.
        self.x = 0
        # Vertical layer offset. Always 0 in Tiled Qt.
        self.y = 0

        # Array of GIDs. tilelayer only.
        self.data = []
        # Array of Objects. objectgroup only.
        self.objects = []

        # Value between 0 and 1
        self.opacity = 0.0

        # "topdown" (default) or "index". objectgroup only.
        self.draworder = ''
