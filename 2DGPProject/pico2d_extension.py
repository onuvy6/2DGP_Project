import math
import pico2d
from sdl2 import *


# for debugging draw
def draw_line(x1,y1,x2,y2,r,g,b):
    SDL_SetRenderDrawColor(pico2d.renderer, r, g, b, 255)
    SDL_RenderDrawLine(pico2d.renderer, x1, y1, x2, y2)
    

def draw_rectangle(x1,y1,x2,y2,r,g,b):
    SDL_SetRenderDrawColor(pico2d.renderer, r, g, b, 255)
    rect = SDL_Rect(int(x1),int(-y2+pico2d.canvas_height-1),int(x2-x1+1),int(y2-y1+1))
    SDL_RenderDrawRect(pico2d.renderer, rect)


def draw_hexagon(x,y,w,h,r,g,b):
    y = pico2d.canvas_height - y
    half_width  = w // 2
    half_height = h // 2
    outside_length = int(half_width * math.tan(math.radians(30)))
    side_length = int(outside_length // math.sin(math.radians(30)))

    SDL_SetRenderDrawColor(pico2d.renderer, r, g, b, 255)
    SDL_RenderDrawLine(pico2d.renderer, x + half_width, y, x + w, y + outside_length)
    SDL_RenderDrawLine(pico2d.renderer, x + w, y + outside_length, x + w, y + outside_length + half_height)
    SDL_RenderDrawLine(pico2d.renderer, x + w, y + outside_length + half_height, x + half_width, y + h)
    SDL_RenderDrawLine(pico2d.renderer, x + half_width, y + h, x, y + outside_length + half_height)
    SDL_RenderDrawLine(pico2d.renderer, x, y + outside_length + half_height, x, y + outside_length)
    SDL_RenderDrawLine(pico2d.renderer, x, y + outside_length, x + half_width, y)
