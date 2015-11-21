import game_framework
import title_state
import map_loader

from pico2d import *


name = "GameState"
image = None

def enter():
    pass


def exit():
    pass


def update():
    pass


def draw():
    clear_canvas()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        pass


def pause():
    pass


def resume():
    pass
