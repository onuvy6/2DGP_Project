import game_framework
import map_loader
import collision

import character_data
import finn_character
import cubchoo_character
import terrorlight_character
import pause_state
import title_state

from pico2d import *
from pico2d_extension import *


name = "GameStateLevel01"


def enter():

    global game_play, game_over, game_clear
    game_play = True
    game_over = False
    game_clear = False


    global background_music 
    background_music = load_music('Resources/Musics/GameState.ogg')
    background_music.set_volume(64)
    background_music.repeat_play()

    global background_image
    background_image = load_image('Resources/States/Background_01.png')

    global background_gameover
    background_gameover = load_image('Resources/States/GameOverState.png')

    global background_gameclear
    background_gameclear = load_image('Resources/States/GameClearState.png')

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
    
    global terrorlights
    terrorlights = [terrorlight_character.Terrorlight() for i in range(5)]


def exit():
    global background_music 
    del (background_music)

    global background_image, pause_image, back_image
    del (background_image)
    del (pause_image)
    del (back_image)

    global background_gameover, background_gameclear
    del (background_gameover)
    del (background_gameclear)

    global map
    del (map)

    global finn
    del (finn)

    global cubchooes, terrorlights
    del (cubchooes)
    del (terrorlights)

    global game_play, game_over, game_clear
    del (game_play)
    del (game_over)
    del (game_clear)


def update(frame_time):
    global game_play, game_over, game_clear
    if not game_play:
        return
 
    if finn.life:
        finn.update(frame_time)
        collision.collision_tile_and_character(map, finn, frame_time)
        collision.collision_object_and_character(map, finn, frame_time)
    else:
        game_play = False
        game_over = True

    for terrorlight in terrorlights:
        terrorlight.update(frame_time)
        if collision.collision_player_and_character(finn, terrorlight):
            if finn.speed > 30:
                finn.speed -= 10
        collision.collision_map_and_character(map, terrorlight, frame_time) 
        collision.collision_object_and_character(map, terrorlight, frame_time)

    for cubchoo in cubchooes:
        cubchoo.update(frame_time) 
        if finn.frame_stop:
            collision.collision_player_and_character(finn, cubchoo)
        else:
            if collision.collision_player_and_character(cubchoo, finn):
                finn.frame_stop = True
        collision.collision_object_and_character(map, cubchoo, frame_time) 
        collision.collision_tile_and_character(map, cubchoo, frame_time)
        if cubchoo.opacify < 0:
            cubchooes.remove(cubchoo)
    
    map.update(frame_time)

    collision_trigger_and_player()
 
    

def draw(frame_time):
     
    global game_play, game_over, game_clear
    clear_canvas()

    background_image.draw(game_framework.width//2, game_framework.height//2)

    
    map.draw_ground()
    map.draw_hexagon_on_point(finn.x, finn.y)
   
    if finn.life:
        finn.draw()
    
    for cubchoo in cubchooes:
        cubchoo.draw()

    for terrorlight in terrorlights:
        terrorlight.draw()

    map.draw_object()
    
    if game_play:
        pause_image.draw(game_framework.width - pause_image.w // 2, game_framework.height - pause_image.h // 2)
        back_image.draw(back_image.w // 2, game_framework.height - back_image.h // 2)
    elif game_over:
        background_gameover.draw(game_framework.width//2, game_framework.height//2)
        back_image.draw(back_image.w // 2, game_framework.height - back_image.h // 2)
    elif game_clear:
        background_gameclear.draw(game_framework.width//2, game_framework.height//2)
        
    update_canvas()


def handle_events(frame_time):

    global game_play, game_over, game_clear
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
            if game_play:
                if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                       game_framework.width - pause_image.w // 2, game_framework.height - pause_image.h // 2,
                                        pause_image.w, pause_image.h):
                    game_framework.push_state(pause_state)
            if game_play or game_over:
                if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                        back_image.w // 2, game_framework.height - back_image.h // 2,
                                        back_image.w, back_image.h):
                    game_framework.change_state(title_state)


def pause():
    pass


def resume():
    pass


def collision_trigger_and_player():

    for layer in map.layers:

        if layer.name == 'Trigger Layer':

            for object in layer.objects:

                object_rect = map.to_object_rect(object)
                player_rect = finn.to_rect()

                if object.name == 'PortalA':
                    if collision.rect_in_rect(*(player_rect + object_rect)):
                        portalB = map.to_trigger('PortalB')
                        portalB_rect = map.to_object_rect(portalB)
                        finn.x, finn.y = portalB_rect[0], portalB_rect[1]
                #elif object.name == 'PortalB':
                #    if collision.rect_in_rect(*(player_rect + object_rect)):
                #        portalA = map.to_trigger('PortalA')
                #        portalA_rect = map.to_object_rect(portalA)
                #        finn.x, finn.y = portalA_rect[0], portalA_rect[1]
