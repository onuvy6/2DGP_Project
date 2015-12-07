import random
import pico2d
import pico2d_extension
import game_framework

from character_data import *


class Terrorlight(CharacterData):

    image = None
    MPS = 10

    def __init__(self):
        CharacterData.__init__(self)
        #super(CharacterData, self).__init__()
        self.load('Resources/Sprites/Terrorlight.json')

        self.x = random.randint(400, 500)
        self.y = random.randint(400, 500)
        self.speed = random.randint(3, 5) * Terrorlight.MPS
        self.state = random.randint(1,8)

        if Terrorlight.image is None:
            Terrorlight.image = pico2d.load_image(self.name)


    def update(self, frame_time):
        CharacterData.update(self, frame_time)
        if self.frame_stop == True:
            self.state = random.randint(1,8)
            self.frame_stop = False


    def draw(self):
        CharacterData.draw(self, Terrorlight.image)

        if game_framework.debug:
            CharacterData.draw_rect(self, 0, 255, 255)
