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
    half_width, half_height = w // 2, h // 2
    s = int(half_width // math.cos(math.radians(30)))
    b = (h - s) // 2 
    SDL_SetRenderDrawColor(pico2d.renderer, r, g, b, 255)
    SDL_RenderDrawLine(pico2d.renderer, x, y - half_height, x + half_width, y - half_height + b)
    SDL_RenderDrawLine(pico2d.renderer, x + half_width, y - half_height + b, x + half_width, y - half_height + b + s)
    SDL_RenderDrawLine(pico2d.renderer, x + half_width, y - half_height + b + s, x, y + half_height)
    SDL_RenderDrawLine(pico2d.renderer, x, y + half_height, x - half_width, y +half_height - b)
    SDL_RenderDrawLine(pico2d.renderer, x - half_width, y + half_height -b, x - half_width, y + half_height - b - s)
    SDL_RenderDrawLine(pico2d.renderer, x - half_width, y + half_height - b - s, x, y - half_height)