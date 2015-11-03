import random

#from pico2d import *
import pico2d

from sdl2 import *


PLAYER_DEFAULT, PLAYER_DOWN, PLAYER_LEFT_DOWN, PLAYER_RIGHT_DOWN, PLAYER_LEFT, PLAYER_RIGHT, PLAYER_UP, PLAYER_LEFT_UP, PLAYER_RIGHT_UP = 0, 1, 2, 3, 4, 5, 6, 7, 8

class Player:
    image = None

    def __init__(self):
        if Player.image == None:
            Player.image = pico2d.load_image('Resources/Sprites/55313.png')
        self.x, self.y = 100, 100
        self.frame = 0
        self.state = PLAYER_DEFAULT
        self.stop_animation = True
        self.viewRect = False
        self.collision = False

    
    def update(self, map):
        if self.stop_animation:
            self.frame = 0
        else:
            self.frame = (self.frame + 1) % 6
        

    def draw(self):
        if self.viewRect:
            self.drawRect(self.x - 23, self.y - 35, self.x + 23, self.y + 35)
        self.image.clip_draw(self.frame * 23, self.image.h - ((self.state+1) * 35), 23, 35, self.x, self.y, 23 * 2, 35 * 2)

    def drawRect(self, x1, y1, x2, y2):
        if self.collision:
            SDL_SetRenderDrawColor(pico2d.renderer, 255, 0, 0, 255)
        else:
            SDL_SetRenderDrawColor(pico2d.renderer, 0, 255, 0, 255)
        rect = SDL_Rect(int(x1),int(-y2+pico2d.canvas_height-1),int(x2-x1+1),int(y2-y1+1))
        SDL_RenderDrawRect(pico2d.renderer, rect)

