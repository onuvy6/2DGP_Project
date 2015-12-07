import random
import math
import pico2d
import pico2d_extension
import game_framework

from particle_data import *


class Maple(ParticleData):
    
    images = []
    MPS = 50
    
    def __init__(self):
        ParticleData.__init__(self)
        #super(ParticleData, self).__init__()
        
        if not Maple.images:
            Maple.images.append(pico2d.load_image('Resources/Particles/Maple_01.png'))
            Maple.images.append(pico2d.load_image('Resources/Particles/Maple_02.png'))

        self.x = random.randint(0, game_framework.width)
        self.y = game_framework.height + random.randint(0, 10)
        self.type = random.randint(0,1)
        self.min_speed = Maple.MPS
        self.max_speed = Maple.MPS * 2
        self.speed = random.randint(self.min_speed, self.max_speed)
        self.scale = random.randint(5,10) * 0.1
        self.width = Maple.images[self.type].w
        self.height = Maple.images[self.type].h

        self.origin_x = self.x
        self.angle = 0
        
    def update(self, frame_time):
        self.angle = (self.angle + self.speed * frame_time) % 360
        self.x = self.origin_x + 10 * self.speed * frame_time * math.sin(math.radians(self.angle))

        ParticleData.update(self, frame_time)


    def draw(self):
        ParticleData.draw(self, Maple.images[self.type])
        if game_framework.debug:
            ParticleData.draw_rect(self, 255, 255, 0)

