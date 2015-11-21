class ObjectData:
    def __init__(self):
        # Incremental id - unique across all objects
        self.id = 0

        # Width in pixels. Ignored if using a gid.
        self.width = 0
        # Height in pixels. Ignored if using a gid.
        self.height = 0

        # String assigned to name field in editor
        self.name = ''
        # String assigned to type field in editor
        self.type = ''

        # Whether object is shown in editor.
        self.visible = True

        # x coordinate in pixels
        self.x = 0
        # y coordinate in pixels
        self.y = 0

        # Angle in degrees clockwise
        self.rotation = 0.0

        # GID, only if object comes from a Tilemap
        self.gid = 0
