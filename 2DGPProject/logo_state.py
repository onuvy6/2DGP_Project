import game_framework
import title_state

from pico2d import *


name = "LogoState"
image = None
logo_time = 0.0

def enter():
    global image
    open_canvas(game_framework.width, game_framework.height)
    image = load_image('Resources/States/kpu_credit.png')


def exit():
     global image
     del (image)
     close_canvas()


def update(frame_time):
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0.0
        game_framework.push_state(title_state)
    logo_time += frame_time


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(game_framework.width//2, game_framework.height//2)
    update_canvas()


def handle_events(frame_time):
    pass


def pause():
    pass


def resume():
    pass
