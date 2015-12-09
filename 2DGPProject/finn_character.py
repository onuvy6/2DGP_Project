import pico2d
import pico2d_extension
import game_framework
import random

from character_data import *


class Finn(CharacterData):

    image = None
    sounds = None
    MPS = 100

    def __init__(self):
        CharacterData.__init__(self)
        #super(CharacterData, self).__init__()
        self.load('Resources/Sprites/Finn.json')
        
        self.x = 320
        self.y = 480
        self.speed = Finn.MPS
        self.frame_time = 0.05

        if Finn.image is None:
            Finn.image = pico2d.load_image(self.name)
            #pico2d_extension.set_texture_color(Finn.image.texture, 255, 255, 255)
        if Finn.sounds is None:
            Finn.sounds = []
            damage_sound = pico2d.load_wav('Resources/Sounds/Damage01.wav')
            damage_sound.set_volume(32)
            Finn.sounds.append(damage_sound)
            
            damage_sound = pico2d.load_wav('Resources/Sounds/Damage02.wav')
            damage_sound.set_volume(32)
            Finn.sounds.append(damage_sound)

            damage_sound = pico2d.load_wav('Resources/Sounds/Damage03.wav')
            damage_sound.set_volume(32)
            Finn.sounds.append(damage_sound)


    def update(self, frame_time):
        if not self.frame_stop:
            pico2d_extension.set_texture_color(Finn.image.texture, 255, 255, 255)
        if self.speed < 100:
            self.speed += 10 * frame_time
        CharacterData.update(self, frame_time)


    def draw(self):
        CharacterData.draw(self, Finn.image)
        if game_framework.debug:
            CharacterData.draw_rect(self, 0, 255, 0)


    def play_hit_sound(self):
        Finn.sounds[random.randint(0,2)].play()


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
        
