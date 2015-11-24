import random
import pico2d
import pico2d_extension

from character_data import *


class Cubchoo(CharacterData):

    image = None

    def __init__(self):
        CharacterData.__init__(self)
        #super(CharacterData, self).__init__()
        self.load('Resources/Sprites/Cubchoo.json')

        self.x = random.randint(400, 500)
        self.y = random.randint(400, 500)
        self.speed = random.randint(1, 3)

        range = (1, 4, 5, 6)
        self.state = range[random.randint(0,3)]

        if Cubchoo.image is None:
            Cubchoo.image = pico2d.load_image(self.name)


    def update(self):
        CharacterData.update(self)
        if self.frame_stop == True:
            range = (1, 4, 5, 6)
            self.state = range[random.randint(1,3)]
            self.frame_stop = False


    def draw(self):
        CharacterData.draw(self, Cubchoo.image)
        CharacterData.draw_rect(self, 255, 0, 0)
