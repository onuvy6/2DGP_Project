import math
import pico2d
from sdl2 import *
from sdl2.sdlimage import *
import ctypes

# for debugging draw
def draw_line(x1,y1,x2,y2):
    SDL_RenderDrawLine(pico2d.renderer, x1, y1, x2, y2)
    

def draw_rectangle(x1,y1,x2,y2):
    rect = SDL_Rect(int(x1),int(-y2+pico2d.canvas_height-1),int(x2-x1+1),int(y2-y1+1))
    SDL_RenderDrawRect(pico2d.renderer, rect)

    
def draw_hexagon(x,y,size):
    hexagons = [get_hexagon_point(x,y,size,0),\
                get_hexagon_point(x,y,size,1),\
                get_hexagon_point(x,y,size,2),\
                get_hexagon_point(x,y,size,3),\
                get_hexagon_point(x,y,size,4),\
                get_hexagon_point(x,y,size,5)
                ]
    draw_line(*(hexagons[0]+hexagons[1]))
    draw_line(*(hexagons[1]+hexagons[2]))
    draw_line(*(hexagons[2]+hexagons[3]))
    draw_line(*(hexagons[3]+hexagons[4]))
    draw_line(*(hexagons[4]+hexagons[5]))
    draw_line(*(hexagons[5]+hexagons[0]))


def get_hexagon_point(x,y,size,i):
    angle_deg = 60 * i + 30
    angle_rad = math.radians(angle_deg)
    return (int(x + size * math.cos(angle_rad)),\
            pico2d.canvas_height - int(y + size * math.sin(angle_rad)) )


def set_color(r,g,b):
    SDL_SetRenderDrawColor(pico2d.renderer, r, g, b, 255)


def set_texture_color(texture, r, g, b):
    SDL_SetTextureColorMod(texture, r, g, b)
