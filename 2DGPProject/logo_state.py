import game_framework
import title_state

from pico2d import *


name = "LogoState"
image = None
logo_time = 0.0

def enter():
    global image
    open_canvas(640, 960)
    image = load_image('Resources/States/kpu_credit.png')


def exit():
     global image
     del (image)
     close_canvas()


def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0.0
        game_framework.push_state(title_state)
    logo_time += 0.01
    delay(0.01)


def draw():
    global image
    clear_canvas()
    image.draw(320, 480)
    update_canvas()


def handle_events():
    pass


def pause():
    pass


def resume():
    pass
