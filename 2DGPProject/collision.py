import math
import character_data


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
    
    intersect_left, intersect_right = 0, 0
    intersect_top, intersect_bottom = 0, 0

    if o1_left <= o2_right and o1_right >= o2_left:
        intersect_left = o1_left > o2_left and o1_left or o2_left
        intersect_right = o1_right < o2_right and o1_right or o2_right

    if o1_top <= o2_bottom and o1_bottom >= o2_top:
        intersect_top = o1_top> o2_top and o1_top or o2_top
        intersect_bottom = o1_bottom > o2_bottom and o1_bottom or o2_bottom

    return intersect_left, intersect_bottom, intersect_right, intersect_top


def collision_map_and_character(map, character):
    for layer in map.layers:
        # objectgroup
        if layer.type == 'objectgroup':
            for object in layer.objects:
                object_rect = map.to_object_rect(object)
                character_rect = character.to_rect()

                if rect_in_rect(*(object_rect + character_rect)):

                    character_width = character_rect[2] - character_rect[0]
                    character_height = character_rect[3] - character_rect[1]
                      
                    if character.state == character_data.CharacterData.CHARACTER_STATE_WALK_LEFT:
                        character.x = object_rect[2] + (character_width // 2 + 1)
                    elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_RIGHT:
                        character.x = object_rect[0] - (character_width // 2 + 1)
                    elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_UP:
                        character.y = object_rect[1] - (character_height // 2 + 1)
                    elif character.state == character_data.CharacterData.CHARACTER_STATE_WALK_DOWN:
                        character.y = object_rect[3] + (character_height // 2 + 1)

                    character.frame_stop = True

                    break