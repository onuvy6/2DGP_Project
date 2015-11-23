import pico2d
import pico2d_extension

from character_data import *


class Finn(CharacterData):

    image = None

    def __init__(self):
        CharacterData.__init__(self)
        #super(CharacterData, self).__init__()
        self.load('Resources/Sprites/Finn.json')
        
        if Finn.image is None:
            Finn.image = pico2d.load_image(self.name)


    def update(self):
        CharacterData.update(self)


    def draw(self):
        CharacterData.draw(self, Finn.image)
        CharacterData.draw_rect(self, 255, 255, 0)

