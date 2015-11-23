import game_framework
import game_state
import map_loader
import collision

import character_data
import finn_character

from pico2d import *
from pico2d_extension import *


name = "TitleState"
image = None
map = None
finn = None

def enter():
    global image
    image = load_image('Resources/States/Background_01.png')

    global map
    map = map_loader.load_map('Resources/Maps/Level_01.json')

    global finn
    finn = finn_character.Finn()

    pass


def exit():
    global map
    del (map)

    global image
    del (image)

    global finn
    del (finn)


def update():
    finn.update()
    collision.collision_map_and_character(map, finn)
    

def draw():
    clear_canvas()
    image.draw(game_framework.width//2, game_framework.height//2)
    map.draw();
    map.draw_hexagon_on_point(finn.x, finn.y)
    finn.draw()
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
