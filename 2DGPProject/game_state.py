import random
import json
import os

import game_framework
from pico2d import *


import tile
from player import Player
from enemy import Enemy

name = "GameState"

font = None

PLAYER_DEFAULT, PLAYER_DOWN, PLAYER_LEFT_DOWN, PLAYER_RIGHT_DOWN, PLAYER_LEFT, PLAYER_RIGHT, PLAYER_UP, PLAYER_LEFT_UP, PLAYER_RIGHT_UP = 0, 1, 2, 3, 4, 5, 6, 7, 8

def enter():
    open_canvas(1024, 800)
    global background
    # background = load_image('Resources/background.png')
    global map
    map = tile.load_tile_map('Resources/prototype_map.json')
    #map = tile.load_tile_map('Resources/test_map.json')

    global enemys
    enemys = [Enemy() for i in range(50)]

    global player
    player = Player()

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
            elif event.key == SDLK_TAB:
                map.viewRect = not map.viewRect
                player.viewRect = not player.viewRect
                for enemy in enemys:
                    enemy.viewRect = not enemy.viewRect
                

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
    for enemy in enemys:
        enemy.update()
    delay(0.01)


def draw():
    clear_canvas()
    # background.draw(0, 0)
    map.draw_all_layer(0, 0)
    player.draw()
    for enemy in enemys:
        enemy.draw()
    update_canvas()
