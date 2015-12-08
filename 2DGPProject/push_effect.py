import pico2d

from effect_data import *


class PushEffect(EffectData):
    
    image = None

    def __init__(self,x,y):
        EffectData.__init__(self)
        self.load('Resources/Effects/Push.json')

        self.x = x
        self.y = y

        if PushEffect.image is None:
            PushEffect.image = pico2d.load_image(self.name)


    def update(self, frame_time):
        EffectData.update(self, frame_time)


    def draw(self):
        EffectData.draw(self, PushEffect.image)
