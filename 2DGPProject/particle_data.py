import json
import random
from pico2d import *
import pico2d_extension
import game_framework


class ParticleData(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.speed = 0
        self.scale = 1.0
        

    def to_rect(self):
        return (self.x - (self.width * self.scale) // 2,   \
                self.y - (self.height * self.scale) // 2,  \
                self.x + (self.width * self.scale) // 2,   \
                self.y + (self.height * self.scale) // 2)


    def update(self, frame_time):
        self.y -= self.speed * frame_time
        if self.y < 0:
            self.y = game_framework.height + random.randint(0, 10)


    def draw(self, image):
        image.clip_draw(0, 0, self.width, self.height,
                        self.x, self.y, int(self.width * self.scale), int(self.height * self.scale))


    def draw_rect(self, r, g, b):
        pico2d_extension.set_color(255, 255, 0)
        pico2d_extension.draw_rectangle(*self.to_rect())
