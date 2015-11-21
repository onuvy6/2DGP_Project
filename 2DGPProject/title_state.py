import game_framework
import game_state
import map_loader

from pico2d import *
from pico2d_extension import *


name = "TitleState"
image = None
map = None

def enter():
    global map
    map = map_loader.load_map('Resources/Maps/prototype_map.json')


def exit():
    global map
    del (map)


def update():
    pass


def draw():
    clear_canvas()
    draw_rectangle(0, 0, 100, 100, 255, 0, 0)
    map.draw();
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        pass


def pause():
    pass


def resume():
    pass
