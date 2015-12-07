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
        self.y = game_framework.height + random.randint(0, 10)
        self.type = random.randint(0,1)
        self.speed = Snow.MPS + random.randint(1,5) * Snow.MPS
        self.scale = random.randint(1,5) * 0.1
        self.width = Snow.image.w
        self.height = Snow.image.h


    def update(self, frame_time):
        ParticleData.update(self, frame_time)


    def draw(self):
        ParticleData.draw(self, Snow.image)
        if game_framework.debug:
            ParticleData.draw_rect(self, 255, 255, 0)

