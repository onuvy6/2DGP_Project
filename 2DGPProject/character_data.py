import json
import pico2d
import pico2d_extension


class CharacterData(object):

    def __init__(self):
        self.name = ''
        self.x = 100
        self.y = 100
        self.frame = 0
        self.state = 0
        self.animations = []
        

    def load(self, name):
        with open(name) as f:
            data = json.load(f)
        
            self.name = data.get('image')
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


    def update(self):
        self.frame = (self.frame + 1) % (self.animations[self.state].framecount)


    def draw(self, image):
        animation = self.animations[self.state]
        image.clip_draw(animation.x + (self.frame * animation.framewidth), (image.h - animation.frameheight) - animation.y,
                        animation.framewidth, animation.frameheight,           
                        self.x, self.y,                                             
                        animation.framewidth, animation.frameheight)


    def draw_rect(self, r, g, b):
        pico2d_extension.draw_rectangle(*self.to_rect() + (r, g, b) )


class AnimationData:

    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.framewidth = 0
        self.frameheight = 0
        self.framecount = 0

