import math
import character_data
import pico2d
import pico2d_extension

def point_in_rect(px,py,rx,ry,rw,rh):
    if px > rx + (rw // 2) or px < rx - (rw // 2):
        return False
    if py > ry + (rh // 2) or py < ry - (rh // 2):
        return False
    return True


def rect_in_rect(o1_left,o1_bottom,o1_right,o1_top,o2_left,o2_bottom,o2_right,o2_top):

    if o1_left > o2_right: return False
    if o1_right < o2_left: return False
    if o1_top < o2_bottom: return False
    if o1_bottom > o2_top: return False

    return True


def get_intersect_rect(o1_left,o1_bottom,o1_right,o1_top,o2_left,o2_bottom,o2_right,o2_top):
    
    left, right, bottom, top = 0, 0, 0, 0

    if rect_in_rect(o1_left,o1_bottom,o1_right,o1_top,o2_left,o2_bottom,o2_right,o2_top):
        if (o1_left < o2_right and o1_right > o2_left):
            left    = (o1_left > o2_left) and o1_left or o2_left
            right   = (o1_right < o2_right) and o1_right or o2_right

        if (o1_top > o2_bottom and o1_bottom < o2_top):
            bottom  = (o1_bottom > o2_bottom) and o1_bottom or o2_bottom
            top     = (o1_top < o2_top) and o1_top or o2_top

        pico2d_extension.set_color(255, 0, 0)
        pico2d_extension.draw_rectangle(left,bottom,right,top)
        pico2d.update_canvas()

    return left, bottom, right, top


def get_intersect_size_hold_object_and_object(ho_left,ho_bottom,ho_right,ho_top,o_left,o_bottom,o_right,o_top):

    rect = get_intersect_rect(ho_left,ho_bottom,ho_right,ho_top,o_left,o_bottom,o_right,o_top)
    
    result_width    = 0
    result_height   = 0

    if rect != (0, 0, 0, 0):
        
        width   = (rect[2] - rect[0]) + 1
        height  = (rect[3] - rect[1]) + 1

        if width > height:
            if rect[3] == ho_top:
                result_height = height
            elif rect[1] == ho_bottom:
                result_height = -height
        else:
            if rect[0] == ho_left:
                result_width = -width
            elif rect[2] == ho_right:
                result_width = width

    return result_width, result_height


def collision_map_and_character(map, character):
    for layer in map.layers:
        if layer.type == 'tilelayer':
            hexagon_index = map.get_hexagon_index_from_point(character.x, character.y)

            x, y = hexagon_index
            
            if (x < 0 or x >= map.width) or (y < 0 or y >= map.height) or layer.data[y][x] == 0:
    
                if character.state == character_data.CharacterData.CHARACTER_STATE_WALK_LEFT:
                    character.x += character.speed
                elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_RIGHT:
                    character.x -= character.speed
                elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_UP:
                    character.y -= character.speed
                elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_UP_LEFT:
                    character.x += character.speed
                    character.y -= character.speed
                elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_UP_RIGHT:
                    character.x -= character.speed
                    character.y -= character.speed
                elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_DOWN:
                    character.y += character.speed
                elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_DOWN_LEFT:
                    character.x += character.speed
                    character.y += character.speed
                elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_DOWN_RIGHT:
                    character.x -= character.speed
                    character.y += character.speed

                character.frame_stop = True

        # objectgroup
        elif layer.type == 'objectgroup':
            if layer.name == 'Collision Layer':
                for object in layer.objects:

                    object_rect = map.to_object_rect(object)
                    character_rect = character.to_rect()

                    size = get_intersect_size_hold_object_and_object(*(object_rect + character_rect))

                    if size != (0, 0):

                        character.x += size[0]
                        character.y += size[1]

                        character.frame_stop = True

                        break      


def collision_player_and_character(player, character):

    player_rect     = player.to_rect()
    character_rect  = character.to_rect()

    size = get_intersect_size_hold_object_and_object(*(character_rect + player_rect))

    if size != (0, 0):
        player.x += size[0]
        player.y += size[1]

        player.frame_stop = True