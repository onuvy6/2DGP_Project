import game_framework
import game_state
import map_loader

from pico2d import *
from pico2d_extension import *


name = "TitleState"
image = None
map = None

def enter():
    global image
    image = load_image('Resources/States/Background_01.png')

    global map
    map = map_loader.load_map('Resources/Maps/Level_01.json')


def exit():
    global map
    del (map)

    global image
    del (image)


def update():
    pass


def draw():
    clear_canvas()
    image.draw(320, 480)
    #draw_hexagon(100, 100, 85, 90, 0, 0, 0)
    map.draw(640, 960);
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        pass


def pause():
    pass


def resume():
    pass
