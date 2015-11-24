import game_framework
import game_state_level_01
import map_loader
import collision

import character_data
import finn_character
import cubchoo_character
import terrorlight_character

from pico2d import *
from pico2d_extension import *


name = "TitleState"

def enter():
    global image
    image = load_image('Resources/States/Background_01.png')

    global map
    map = map_loader.load_map('Resources/Maps/Title.json')

    global cubchooes
    cubchooes = [cubchoo_character.Cubchoo() for i in range(3)]

    global terrorlights
    terrorlights = [terrorlight_character.Terrorlight() for i in range(3)]


def exit():
    del (image)
    
    del (map)

    del (cubchooes)


def update():

    for cubchoo in cubchooes:
        cubchoo.update()
        collision.collision_map_and_character(map, cubchoo)        
    
    for terrorlight in terrorlights:
        terrorlight.update()
        collision.collision_map_and_character(map, terrorlight) 


def draw():
    clear_canvas()

    image.draw(game_framework.width//2, game_framework.height//2)

    map.draw_low()
    
    for cubchoo in cubchooes:
        cubchoo.draw()

    for terrorlight in terrorlights:
        terrorlight.draw()

    map.draw_high()

    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        pass


def pause():
    pass


def resume():
    pass
