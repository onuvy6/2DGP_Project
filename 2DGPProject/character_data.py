import json
from pico2d import *
import pico2d_extension


class CharacterData(object):

    CHARACTER_STATE_WAIT,               \
    CHARACTER_STATE_WALK_DOWN,          \
    CHARACTER_STATE_WALK_DOWN_LEFT,     \
    CHARACTER_STATE_WALK_DOWN_RIGHT,    \
    CHARACTER_STATE_WALK_LEFT,          \
    CHARACTER_STATE_WALK_RIGHT,         \
    CHARACTER_STATE_WALK_UP,            \
    CHARACTER_STATE_WALK_UP_LEFT,       \
    CHARACTER_STATE_WALK_UP_RIGHT = 0, 1, 2, 3, 4, 5, 6, 7, 8

    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.speed = 0
        self.frame = 0
        self.frame_stop = False
        self.state = CharacterData.CHARACTER_STATE_WAIT
        self.animations = []
        self.life = True
        
        self.character_state_type = {
            CharacterData.CHARACTER_STATE_WAIT : self.character_state_wait,
            CharacterData.CHARACTER_STATE_WALK_DOWN : self.character_state_walk_down,
            CharacterData.CHARACTER_STATE_WALK_DOWN_LEFT : self.character_state_walk_down_left,
            CharacterData.CHARACTER_STATE_WALK_DOWN_RIGHT : self.character_state_walk_down_right,
            CharacterData.CHARACTER_STATE_WALK_LEFT : self.character_state_walk_left,
            CharacterData.CHARACTER_STATE_WALK_RIGHT : self.character_state_walk_right,
            CharacterData.CHARACTER_STATE_WALK_UP : self.character_state_walk_up,
            CharacterData.CHARACTER_STATE_WALK_UP_LEFT : self.character_state_walk_up_left,
            CharacterData.CHARACTER_STATE_WALK_UP_RIGHT : self.character_state_walk_up_right,
        }
        

    def load(self, name):
        with open(name) as f:
            data = json.load(f)
        
            self.name = data.get('image')
            self.speed = data.get('speed')
            animations = data.get('animations')
            if animations is not None:
                for animation in animations:
                    animation_data = AnimationData()

                    animation_data.name = animation.get('name')
                    animation_data.x = animation.get('x')
                    animation_data.y = animation.get('y')
                    animation_data.framewidth = animation.get('framewidth')
                    animation_data.frameheight = animation.get('frameheight')
                    animation_data.framecount = animation.get('framecount')

                    self.animations.append(animation_data)


    def to_rect(self):
        animation   = self.animations[self.state]
        framewidth  = animation.framewidth
        frameheight = animation.frameheight
        return (self.x - framewidth // 2,   \
                self.y - frameheight // 2,  \
                self.x + framewidth // 2,   \
                self.y + frameheight // 2)


    def update(self, frame_time):
        if self.frame_stop == False:
            self.frame = (self.frame + 1) % (self.animations[self.state].framecount)
            self.character_state_type[self.state](frame_time)

    
    def character_state_wait(self, frame_time):
        pass


    def character_state_walk_down(self, frame_time):
        self.y -= self.speed * frame_time


    def character_state_walk_down_left(self, frame_time):
        self.character_state_walk_down(frame_time)
        self.character_state_walk_left(frame_time)


    def character_state_walk_down_right(self, frame_time):
        self.character_state_walk_down(frame_time)
        self.character_state_walk_right(frame_time)


    def character_state_walk_left(self, frame_time):
        self.x -= self.speed * frame_time


    def character_state_walk_right(self, frame_time):
        self.x += self.speed * frame_time


    def character_state_walk_up(self, frame_time):
        self.y += self.speed * frame_time


    def character_state_walk_up_left(self, frame_time):
        self.character_state_walk_up(frame_time)
        self.character_state_walk_left(frame_time)


    def character_state_walk_up_right(self, frame_time):
        self.character_state_walk_up(frame_time)
        self.character_state_walk_right(frame_time)


    def draw(self, image):
        animation = self.animations[self.state]
        image.clip_draw(animation.x + (self.frame * animation.framewidth), (image.h - animation.frameheight) - animation.y,
                        animation.framewidth, animation.frameheight,           
                        self.x, self.y,                                             
                        animation.framewidth, animation.frameheight)


    def draw_rect(self, r, g, b):
        pico2d_extension.set_color(r, g, b)
        pico2d_extension.draw_rectangle(*self.to_rect())

        
    def change_state(self, state):
        self.state = state
        self.frame_stop = False


class AnimationData:

    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.framewidth = 0
        self.frameheight = 0
        self.framecount = 0

