import game_framework
import collision


from pico2d import *
from pico2d_extension import *


name = "PauseState"

def enter():
    global background_image
    background_image = load_image('Resources/States/PauseState.png')

    global pause_image
    pause_image = load_image('Resources/Images/Pause.png')


def exit():
    global background_image
    del (background_image)
    
    global pause_image
    del (pause_image)


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()


    game_framework.stack[1].draw(frame_time)
    background_image.draw(game_framework.width//2, game_framework.height//2)

    pause_image.draw(game_framework.width - pause_image.w // 2, game_framework.height - pause_image.h // 2)

    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                    game_framework.width - pause_image.w // 2, game_framework.height - pause_image.h // 2,
                                    pause_image.w, pause_image.h):
                game_framework.pop_state()
                break


def pause():
    pass


def resume():
    pass