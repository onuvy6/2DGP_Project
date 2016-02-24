import math
import pico2d
from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlttf import *
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


class Font:
    def __init__(self, name, size=20):
        #print('font' + name + 'loaded')
        self.font = TTF_OpenFont(name.encode('utf-8'), size)

    def draw(self, x, y, str, color=(0,0,0)):
        sdl_color = SDL_Color(color[0], color[1], color[2])
        sdl_bgcolor = SDL_Color(50, 50, 50)
        str = '   "' + str + '"   '
        #print(str)
        surface = TTF_RenderUTF8_Shaded(self.font, str.encode('utf-8'), sdl_color, sdl_bgcolor)
        #surface = TTF_RenderUTF8_Blended(self.font, str.encode('utf-8'), sdl_color)
        texture = SDL_CreateTextureFromSurface(pico2d.renderer, surface)
        SDL_FreeSurface(surface)
        image = pico2d.Image(texture)
        if (x - image.w // 2 < 0):
            x += (image.w // 2 - x)
        elif (x + image.w //2 > pico2d.canvas_width):
            x -= (image.w // 2 - (pico2d.canvas_width - x) )
        
        image.draw(x, y)

        
def load_font(name, size = 20):
    font = Font(name, size)
    return font
