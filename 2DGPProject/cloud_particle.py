import random
import math
import pico2d

from particle_data import *


class Cloud(ParticleData):

    image = None
    image_half_width = 0

    DIRECTION_LEFT, DIRECTION_RIGHT = 0, 1

    MPS = 10

    def __init__(self):
        ParticleData.__init__(self)

        if not Cloud.image:
            Cloud.image = pico2d.load_image('Resources/Particles/Cloud.png')
            Cloud.image_half_width = Cloud.image.w // 2
            Cloud.image.opacify(0.7)

        self.get_cloud_position()

        self.min_speed = Cloud.MPS
        self.max_speed = Cloud.MPS * 5
        
        self.speed = random.randint(self.min_speed, self.max_speed)
        self.scale = random.randint(5, 10) * 0.1
        self.width = Cloud.image.w
        self.height = Cloud.image.h
  

    def update(self, frame_time):

        if self.direction == Cloud.DIRECTION_LEFT:
            self.x -= (self.speed * frame_time)
        else:
            self.x += (self.speed * frame_time)

        if self.x < -(Cloud.image_half_width * self.scale) or \
            self.x > (Cloud.image_half_width * self.scale) + pico2d.get_canvas_width():
            self.get_cloud_position()
        #ParticleData.update(self, frame_time)


    def draw(self):
        ParticleData.draw(self, Cloud.image)


    def get_cloud_position(self):
        self.direction = random.randint(0,1)
        if self.direction == Cloud.DIRECTION_LEFT:
            self.x = (Cloud.image_half_width * self.scale) + pico2d.get_canvas_width()
        else:
            self.x = -(Cloud.image_half_width * self.scale)
        self.y = random.randint(7, 10) * 0.1 * pico2d.get_canvas_height()