import random
import math
import pico2d
import pico2d_extension
import game_framework

from particle_data import *


class Snow(ParticleData):
    
    image = None
    MPS = 50

    def __init__(self):
        ParticleData.__init__(self)
        #super(ParticleData, self).__init__()
        
        if not Snow.image:
            Snow.image = pico2d.load_image('Resources/Particles/Snow.png')
            
        self.x = random.randint(0, game_framework.width)
        self.y = game_framework.height + random.randint(0, 30)
        self.type = random.randint(0,1)
        self.min_speed = Snow.MPS
        self.max_speed = Snow.MPS * 5
        self.speed = random.randint(self.min_speed, self.max_speed)
        self.scale = random.randint(1,5) * 0.1
        self.width = Snow.image.w
        self.height = Snow.image.h


    def update(self, frame_time):
        ParticleData.update(self, frame_time)


    def draw(self):
        ParticleData.draw(self, Snow.image)
        if game_framework.debug:
            ParticleData.draw_rect(self, 255, 255, 0)

