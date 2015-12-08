import json


class EffectData(object):
    
    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.frame = 0
        self.destroyed = False

    
    def load(self, name):
        with open(name) as f:
            data = json.load(f)


    def update(self, frame_time):
        pass


    def draw(self):
        pass

