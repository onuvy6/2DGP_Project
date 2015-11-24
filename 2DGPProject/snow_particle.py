import random
import math
import pico2d
import pico2d_extension
import game_framework

from particle_data import *


class Snow(ParticleData):
    
    image = None
    
    def __init__(self):
        ParticleData.__init__(self)
        #super(ParticleData, self).__init__()
        
        if not Snow.image:
            Snow.image = pico2d.load_image('Resources/Particles/Snow.png')
            
        self.x = random.randint(0, game_framework.width)
        self.y = game_framework.height + random.randint(0, 10)
        self.type = random.randint(0,1)
        self.speed = 5 + random.randint(1,5)
        self.scale = random.randint(1,5) * 0.1
        self.width = Snow.image.w
        self.height = Snow.image.h

        self.origin_x = self.x
        self.angle = 0
        
    def update(self):
        self.angle = (self.angle + 1) % 360
        self.x = self.origin_x + self.speed * math.sin(math.radians(self.angle))

        ParticleData.update(self)


    def draw(self):
        ParticleData.draw(self, Snow.image)
        ParticleData.draw_rect(self, 255, 255, 0)

