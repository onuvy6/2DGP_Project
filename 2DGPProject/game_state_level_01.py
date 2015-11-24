import game_framework
import map_loader
import collision

import character_data
import finn_character
import cubchoo_character
import pause_state
import title_state

from pico2d import *
from pico2d_extension import *


name = "GameStateLevel01"

def enter():
    global background_image
    background_image = load_image('Resources/States/Background_01.png')

    global pause_image
    pause_image = load_image('Resources/Images/Pause.png')

    global back_image
    back_image = load_image('Resources/Images/Back.png')

    global map
    map = map_loader.load_map('Resources/Maps/Level_01.json')

    global finn
    finn = finn_character.Finn()

    global cubchooes
    cubchooes = [cubchoo_character.Cubchoo() for i in range(10)]


def exit():
    global background_image, pause_image, back_image
    del (background_image)
    del (pause_image)
    del (back_image)

    global map
    del (map)

    global finn, cubchooes
    del (finn)
    del (cubchooes)


def update(frame_time):

    finn.update()
    collision.collision_map_and_character(map, finn)

    for cubchoo in cubchooes:
        cubchoo.update()
        if collision.collision_character_and_character(finn, cubchoo):
            pass
        collision.collision_map_and_character(map, cubchoo)        
    

def draw(frame_time):
    clear_canvas()

    background_image.draw(game_framework.width//2, game_framework.height//2)

    map.draw_low()
    map.draw_hexagon_on_point(finn.x, finn.y)

    finn.draw()

    for cubchoo in cubchooes:
        cubchoo.draw()

    map.draw_high()

    pause_image.draw(game_framework.width - pause_image.w // 2, game_framework.height - pause_image.h // 2)
    back_image.draw(back_image.w // 2, game_framework.height - back_image.h // 2)

    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            state = finn.get_state_from_key(event.key)
            if state is not None:
                finn.change_state(state)

        elif event.type == SDL_KEYUP:
            if event.key == finn.get_key_from_state():
                finn.frame_stop = True

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                    game_framework.width - pause_image.w // 2, game_framework.height - pause_image.h // 2,
                                    pause_image.w, pause_image.h):
                game_framework.push_state(pause_state)
            elif collision.point_in_rect(event.x, game_framework.height - event.y, \
                                    back_image.w // 2, game_framework.height - back_image.h // 2,
                                    back_image.w, back_image.h):
                game_framework.change_state(title_state)


def pause():
    pass


def resume():
    pass
