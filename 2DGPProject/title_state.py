import game_framework
import game_state
import map_loader
import finn_character

from pico2d import *
from pico2d_extension import *


name = "TitleState"
image = None
map = None
finn = None

def enter():
    global image
    image = load_image('Resources/States/Background_01.png')

    global map
    map = map_loader.load_map('Resources/Maps/Level_01.json')

    global finn
    finn = finn_character.Finn()

    pass


def exit():
    global map
    del (map)

    global image
    del (image)

    global finn
    del (finn)


def update():
    finn.update()


def draw():
    clear_canvas()
    image.draw(320, 480)
    map.draw(640, 960);
    finn.draw()
    map.collision(finn.x, finn.y)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                finn.state = 4
                finn.x -= 3
            elif event.key == SDLK_RIGHT:
                finn.state = 5
                finn.x += 3
            elif event.key == SDLK_UP:
                finn.state = 6
                finn.y += 3
            elif event.key == SDLK_DOWN:
                finn.state = 1
                finn.y -= 3

        elif event.type is SDL_KEYUP:
            pass


def pause():
    pass


def resume():
    pass
