import game_framework
import game_state
import map_loader
import collision

import character_data
import finn_character
import cubchoo_character

from pico2d import *
from pico2d_extension import *


name = "TitleState"

def enter():
    global image
    image = load_image('Resources/States/Background_01.png')

    global map
    map = map_loader.load_map('Resources/Maps/Level_02.json')

    global finn
    finn = finn_character.Finn()

    global cubchooes
    cubchooes = [cubchoo_character.Cubchoo() for i in range(10)]


def exit():
    del (image)
    
    del (map)

    del (finn)
    del (cubchooes)


def update():

    finn.update()
    collision.collision_map_and_character(map, finn)

    for cubchoo in cubchooes:
        cubchoo.update()
        collision.collision_map_and_character(map, cubchoo)        
    

def draw():
    clear_canvas()

    image.draw(game_framework.width//2, game_framework.height//2)

    map.draw_low()
    map.draw_hexagon_on_point(finn.x, finn.y)

    finn.draw()

    for cubchoo in cubchooes:
        cubchoo.draw()

    map.draw_high()

    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            state = finn.get_state_from_key(event.key)
            if state is not None:
                finn.change_state(state)

        elif event.type == SDL_KEYUP:
            if event.key == finn.get_key_from_state():
                finn.frame_stop = True


def pause():
    pass


def resume():
    pass
