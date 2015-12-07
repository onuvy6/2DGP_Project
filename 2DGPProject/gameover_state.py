import game_framework
import collision
import title_state

from pico2d import *
from pico2d_extension import *


name = "GameOverState"

def enter():
    global background_image
    background_image = load_image('Resources/States/PauseState.png')

    global back_image
    back_image = load_image('Resources/Images/Back.png')


def exit():
    global background_image
    del (background_image)
    
    global back_image
    del (back_image)


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()


    game_framework.stack[1].draw(frame_time)
    background_image.draw(game_framework.width//2, game_framework.height//2)

    back_image.draw(back_image.w // 2, game_framework.height - back_image.h // 2)

    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                    back_image.w // 2, game_framework.height - back_image.h // 2,
                                    back_image.w, back_image.h):
                game_framework.change_state(title_state)
                break


def pause():
    pass


def resume():
    pass