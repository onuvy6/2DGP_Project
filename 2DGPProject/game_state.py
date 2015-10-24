import random
import json
import os

import game_framework
from pico2d import *

import tile

name = "GameState"

font = None


def enter():
    open_canvas();
    global background
    background = tile.load_tile_map('Resources/test_map.json')


def exit():
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events():
    pass


def update():
    delay(0.01)


def draw():
    background.draw_all_layer(0, 0)
    update_canvas()
