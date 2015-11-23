import pico2d
import pico2d_extension

from character_data import *


class Finn(CharacterData):

    image = None

    def __init__(self):
        CharacterData.__init__(self)
        #super(CharacterData, self).__init__()
        self.load('Resources/Sprites/Finn.json')
        
        if Finn.image is None:
            Finn.image = pico2d.load_image(self.name)


    def update(self):
        if self.frame_stop == False:
            if self.state == CharacterData.CHARACTER_STATE_WALK_DOWN:
                self.y -= 3
            elif self.state == CharacterData.CHARACTER_STATE_WALK_UP:
                self.y += 3
            elif self.state == CharacterData.CHARACTER_STATE_WALK_LEFT:
                self.x -= 3
            elif self.state == CharacterData.CHARACTER_STATE_WALK_RIGHT:
                self.x += 3
        CharacterData.update(self)


    def draw(self):
        CharacterData.draw(self, Finn.image)
        CharacterData.draw_rect(self, 255, 255, 0)


    def is_valid_key(self, key):
        return key == SDLK_LEFT or      \
                key == SDLK_RIGHT or    \
                key == SDLK_UP or       \
                key == SDLK_DOWN


    def get_state_from_key(self, key):
        key_to_state_type = {
            SDLK_DOWN : CharacterData.CHARACTER_STATE_WALK_DOWN,
            #SDLK_DOWN | SDLK_LEFT : CharacterData.CHARACTER_STATE_WALK_DOWN_LEFT,
            #SDLK_DOWN | SDLK_RIGHT : CharacterData.CHARACTER_STATE_WALK_DOWN_RIGHT,
            SDLK_UP : CharacterData.CHARACTER_STATE_WALK_UP,
            #SDLK_UP | SDLK_LEFT : CharacterData.CHARACTER_STATE_WLAK_UP_LEFT,
            #SDLK_UP | SDLK_RIGHT : CharacterData.CHARACTER_STATE_WALK_UP_RIGHT,
            SDLK_LEFT : CharacterData.CHARACTER_STATE_WALK_LEFT,
            SDLK_RIGHT : CharacterData.CHARACTER_STATE_WALK_RIGHT,
        }
        if self.is_valid_key(key):
            return key_to_state_type[key]
        return None
      

    def get_key_from_state(self):
        state_to_key_type = {
            CharacterData.CHARACTER_STATE_WAIT : None,
            CharacterData.CHARACTER_STATE_WALK_DOWN : SDLK_DOWN,
            #CharacterData.CHARACTER_STATE_WALK_DOWN_LEFT : SDLK_DOWN | SDLK_LEFT,
            #CharacterData.CHARACTER_STATE_WALK_DOWN_RIGHT : SDLK_DOWN | SDLK_RIGHT,
            CharacterData.CHARACTER_STATE_WALK_UP : SDLK_UP,
            #CharacterData.CHARACTER_STATE_WLAK_UP_LEFT : SDLK_UP | SDLK_LEFT,
            #CharacterData.CHARACTER_STATE_WALK_UP_RIGHT : SDLK_UP | SDLK_RIGHT,
            CharacterData.CHARACTER_STATE_WALK_LEFT : SDLK_LEFT,
            CharacterData.CHARACTER_STATE_WALK_RIGHT : SDLK_RIGHT,
        }
        return state_to_key_type[self.state]
        
