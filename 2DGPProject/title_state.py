import game_framework
import game_state_level_01
import map_loader
import collision

import character_data
import finn_character
import cubchoo_character
import terrorlight_character
import maple_particle
import snow_particle
import cloud_particle
import effect_handler
import damage_effect
import push_effect
import warp_effect

from pico2d import *
from pico2d_extension import *


name = "TitleState"

def enter():
    global background_music 
    background_music = load_music('Resources/Musics/TitleState.ogg')
    background_music.set_volume(64)
    background_music.repeat_play()

    global background_image
    background_image = load_image('Resources/States/Background_01.png')

    global game_start_image
    game_start_image = load_image('Resources/Images/GameStart.png')

    global exit_image
    exit_image = load_image('Resources/Images/Exit.png')

    global map
    map = map_loader.load_map('Resources/Maps/Title.json')

    global effects
    effects = effect_handler.EffectHandler()

    global cubchooes
    cubchooes = [cubchoo_character.Cubchoo() for i in range(3)]

    global terrorlights
    terrorlights = [terrorlight_character.Terrorlight() for i in range(3)]

    global maples
    maples = [maple_particle.Maple() for i in range(10)]

    global snows
    snows = [snow_particle.Snow() for i in range(50)]

    global clouds
    clouds = [cloud_particle.Cloud() for i in range(10)]


def exit():
    global background_music
    del (background_music)

    global background_image
    del (background_image)
    
    global game_start_image, exit_image
    del (game_start_image)
    del (exit_image)

    global map
    del (map)

    global effects
    del (effects)
    
    global cubchooes, terrorlights
    del (cubchooes)
    del (terrorlights)

    global maples, snows, clouds
    del(maples)
    del(snows)
    del(clouds)


def update(frame_time):

    for cubchoo in cubchooes:
        cubchoo.update(frame_time)
        collision.collision_object_and_character(map, cubchoo, frame_time)
        collision.collision_tile_and_character(map, cubchoo, frame_time)        
        if not cubchoo.life:
            cubchooes.remove(cubchoo)
    
    for terrorlight in terrorlights:
        terrorlight.update(frame_time)
        collision.collision_map_and_character(map, terrorlight, frame_time)
        collision.collision_object_and_character(map, terrorlight, frame_time)
        #collision.collision_tile_and_character(map, terrorlight, frame_time) 

    map.update(frame_time)

    for maple in maples:
        maple.update(frame_time)

    for snow in snows:
        snow.update(frame_time)

    for cloud in clouds:
        cloud.update(frame_time)

    effects.update(frame_time)


def draw(frame_time):
    clear_canvas()

    background_image.draw(game_framework.width//2, game_framework.height//2)

    map.draw_ground()

    for cubchoo in cubchooes:
        cubchoo.draw()

    for terrorlight in terrorlights:
        terrorlight.draw()

    map.draw_object()
    
    effects.draw()

    for maple in maples:
        maple.draw()

    for snow in snows:
        snow.draw()

    for cloud in clouds:
        cloud.draw()

    game_start_image.draw(game_framework.width // 2, game_framework.height * 0.3)
    exit_image.draw(game_framework.width - exit_image.w // 2, game_framework.height - exit_image.h // 2)

    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                    game_framework.width // 2 - game_start_image.w // 2, game_framework.height * 0.3 + game_start_image.h // 2,
                                    game_start_image.w, game_start_image.h):
                game_framework.change_state(game_state_level_01)
            elif collision.point_in_rect(event.x, game_framework.height - event.y, \
                                    game_framework.width - exit_image.w // 2, game_framework.height - exit_image.h // 2,
                                         exit_image.w, exit_image.h):
                game_framework.quit()


def pause():
    pass


def resume():
    pass
