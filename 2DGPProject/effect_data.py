import json


class EffectData(object):
    
    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.frame = 0
        self.destroyed_time = 0
        self.destroyed = False

    
    def load(self, name):
        with open(name) as f:
            data = json.load(f)

            self.name = data.get('image')
            self.framewidth = data.get('framewidth')
            self.frameheight = data.get('frameheight')
            self.framecount = data.get('framecount')
            self.destroyed_time = data.get('time')


    def update(self, frame_time):
        self.destroyed_time -= frame_time
        if self.destroyed_time < 0:
            self.destroyed = True
        self.frame = (self.frame + 1) % (self.framecount)


    def draw(self, image):
        image.clip_draw(self.frame * self.framewidth, 0,
                        self.framewidth, self.frameheight,
                        self.x, self.y,
                        self.framewidth, self.frameheight)

