import pico2d
from sdl2 import *


# for debugging draw
def draw_rectangle(x1,y1,x2,y2,r,g,b):
    SDL_SetRenderDrawColor(pico2d.renderer, r, g, b, 255)
    rect = SDL_Rect(int(x1),int(-y2+pico2d.canvas_height-1),int(x2-x1+1),int(y2-y1+1))
    SDL_RenderDrawRect(pico2d.renderer, rect)
