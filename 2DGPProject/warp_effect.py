import pico2d

from effect_data import *


class WarpEffect(EffectData):
    
    image = None
    sound = None

    def __init__(self,x,y):
        EffectData.__init__(self)
        self.load('Resources/Effects/Warp.json')

        self.x = x
        self.y = y

        if WarpEffect.image is None:
            WarpEffect.image = pico2d.load_image(self.name)
        if WarpEffect.sound is None:
            WarpEffect.sound = pico2d.load_wav('Resources/Sounds/Warp.wav')
            WarpEffect.sound.set_volume(64)


    def update(self, frame_time):
        EffectData.update(self, frame_time)


    def draw(self):
        EffectData.draw(self, WarpEffect.image)
