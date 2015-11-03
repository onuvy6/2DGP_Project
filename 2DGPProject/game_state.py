import random
import json
import os

import game_framework
from pico2d import *


import tile_loader
from player import Player
from enemy import Enemy
from terrorlight import TerrorLight

name = "GameState"

font = None

PLAYER_DEFAULT, PLAYER_DOWN, PLAYER_LEFT_DOWN, PLAYER_RIGHT_DOWN, PLAYER_LEFT, PLAYER_RIGHT, PLAYER_UP, PLAYER_LEFT_UP, PLAYER_RIGHT_UP = 0, 1, 2, 3, 4, 5, 6, 7, 8

def enter():
    open_canvas(1024, 800)
    global background
    # background = load_image('Resources/background.png')
    global map
    map = tile_loader.load_tile_map('Resources/Maps/prototype_map.json')
    #map = tile_loader.load_tile_map('Resources/test_map.json')

    global enemys
    enemys = [Enemy() for i in range(20)]

    global terrorlights
    terrorlights = [TerrorLight() for i in range(30)]

    global player
    player = Player()

    global do_not_draw_enemy
    do_not_draw_enemy = False

    global do_not_draw_terrorlight
    do_not_draw_terrorlight = True

    hide_lattice()
    

def exit():
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                player.state = PLAYER_LEFT
                player.stop_animation = False
            elif event.key == SDLK_RIGHT:
                player.state = PLAYER_RIGHT
                player.stop_animation = False
            elif event.key == SDLK_UP:
                player.state = PLAYER_UP
                player.stop_animation = False
            elif event.key == SDLK_DOWN:
                player.state = PLAYER_DOWN
                player.stop_animation = False
            elif event.key == SDLK_v:
                map.viewRect = not map.viewRect
                player.viewRect = not player.viewRect
                for enemy in enemys:
                    enemy.viewRect = not enemy.viewRect
                for terrorlight in terrorlights:
                    terrorlight.viewRect = not terrorlight.viewRect
            elif event.key == SDLK_e:
                global do_not_draw_enemy
                do_not_draw_enemy = not do_not_draw_enemy
            elif event.key == SDLK_t:
                global do_not_draw_terrorlight
                do_not_draw_terrorlight = not do_not_draw_terrorlight

                

        elif event.type == SDL_KEYUP:
            player_state_with_key = {
                PLAYER_DOWN : SDLK_DOWN,
                PLAYER_UP : SDLK_UP,
                PLAYER_LEFT : SDLK_LEFT,
                PLAYER_RIGHT : SDLK_RIGHT
            }
            if event.key == player_state_with_key.get(player.state):
                player.stop_animation = True
            

def update():
    if player.stop_animation != True:
        if player.state == PLAYER_DOWN:
            player.y -= 3
        elif player.state == PLAYER_UP:
            player.y += 3
        elif player.state == PLAYER_RIGHT:
            player.x += 3
        elif player.state == PLAYER_LEFT:
            player.x -= 3
    player.update(map)
    player.collision = False

    if not do_not_draw_enemy:
        for enemy in enemys:
            enemy.update()
            # 충돌 검출
            player_left, player_right = player.x - 23, player.x + 23
            player_top, player_bottom = player.y + 35, player.y - 35

            enemy_left, enemy_right = enemy.x - 26, enemy.x + 26
            enemy_top, enemy_bottom = enemy.y + 28, enemy.y - 28 
        
            enemy.collision = False

            if ((player_left <= enemy_right) and (player_top > enemy_bottom) and (player_right >= enemy_left) and (player_bottom < enemy_top)):
                player.collision, enemy.collision = True, True

    if not do_not_draw_terrorlight:
        for terrorlight in terrorlights:
            terrorlight.update()
            # 충돌 검출
            player_left, player_right = player.x - 23, player.x + 23
            player_top, player_bottom = player.y + 35, player.y - 35

            terrorlight_left, terrorlight_right = terrorlight.x - 36, terrorlight.x + 36
            terrorlight_top, terrorlight_bottom = terrorlight.y + 30, terrorlight.y - 30 
        
            terrorlight.collision = False

            if ((player_left <= terrorlight_right) and (player_top > terrorlight_bottom) and (player_right >= terrorlight_left) and (player_bottom < terrorlight_top)):
                player.collision, terrorlight.collision = True, True

    delay(0.01)


def draw():
    clear_canvas()
    # background.draw(0, 0)
    map.draw_all_layer(0, 0)
    player.draw()
    if not do_not_draw_enemy:
        for enemy in enemys:
            enemy.draw()

    if not do_not_draw_terrorlight:
        for terrorlight in terrorlights:
            terrorlight.draw()
    update_canvas()
