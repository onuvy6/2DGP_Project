import random

#from pico2d import *
import pico2d

from sdl2 import *


ENEMY_DEFAULT, ENEMY_DOWN, ENEMY_LEFT_DOWN, ENEMY_RIGHT_DOWN, ENEMY_LEFT, ENEMY_RIGHT, ENEMY_UP, ENEMY_LEFT_UP, ENEMY_RIGHT_UP = 0, 1, 2, 3, 4, 5, 6, 7, 8

class TerrorLight:
    image = None

    def __init__(self):
        if TerrorLight.image == None:
            TerrorLight.image = pico2d.load_image('Resources/Sprites/terrorlight.png')
        self.x, self.y = random.randint(100, 900), random.randint(100, 800)
        self.frame = 0
        self.state = ENEMY_DEFAULT #random.randint(0, 8)
        self.stop_animation = False
        self.viewRect = False
        self.wait_frame = random.randint(10, 30)
        self.action_frame = random.randint(50, 100)
        self.collision = False

    
    def update(self):
        if self.stop_animation:
            self.frame = 0
        else:
            self.frame = (self.frame + 1) % 3

        self.action_frame -= 1
        if self.action_frame < 0:
            self.state = ENEMY_DEFAULT

        enemy_state = {
            ENEMY_DEFAULT : self.action_default,
            ENEMY_DOWN : self.action_down,
            ENEMY_LEFT_DOWN : self.action_left_down,
            ENEMY_RIGHT_DOWN : self.action_right_down,
            ENEMY_LEFT : self.action_left,
            ENEMY_RIGHT : self.action_right,
            ENEMY_UP : self.action_up,
            ENEMY_LEFT_UP : self.action_left_up,
            ENEMY_RIGHT_UP : self.action_right_up
        }
        enemy_state[self.state]()
        
    def action_default(self):
        self.wait_frame -= 1
        if self.wait_frame < 0:
            self.wait_frame = random.randint(10, 30)
            self.action_frame = random.randint(50, 100)
            self.state = random.randint(0, 8)

    def action_left(self):
        self.x -= 3
        if self.x < 0:
            self.x = 0
            self.state = ENEMY_DEFAULT

        
    def action_right(self):
        self.x += 3
        if self.x > 1024:
            self.x = 1024
            self.state = ENEMY_DEFAULT


    def action_up(self):
        self.y += 3
        if self.y > 800:
            self.y = 800
            self.state = ENEMY_DEFAULT


    def action_down(self):
        self.y -= 3
        if self.y < 0:
            self.y = 0
            self.state = ENEMY_DEFAULT

    
    def action_left_up(self):
        self.action_left()
        self.action_up()

    def action_left_down(self):
        self.action_left()
        self.action_down()


    def action_right_up(self):
        self.action_right()
        self.action_up()


    def action_right_down(self):
        self.action_right()
        self.action_down()


    def draw(self):
        if self.viewRect:
            self.drawRect(self.x - 36, self.y - 30, self.x + 36, self.y + 30)
        self.image.clip_draw(self.frame * 36, self.image.h - ((self.state+1) * 30), 36, 30, self.x, self.y, 36 * 2, 30 * 2)


    def drawRect(self, x1, y1, x2, y2):
        if self.collision:
            SDL_SetRenderDrawColor(pico2d.renderer, 255, 0, 0, 255)
        else:
            SDL_SetRenderDrawColor(pico2d.renderer, 255, 255, 0, 255)
        rect = SDL_Rect(int(x1),int(-y2+pico2d.canvas_height-1),int(x2-x1+1),int(y2-y1+1))
        SDL_RenderDrawRect(pico2d.renderer, rect)

