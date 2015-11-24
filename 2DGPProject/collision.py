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
            if layer.name == 'Object Layer 1':
                for object in layer.objects:
                    object_rect = map.to_object_rect(object)
                    character_rect = character.to_rect()

                    if rect_in_rect(*(object_rect + character_rect)):

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

                        break                      


def collision_character_and_character(character1, character2):

    character1_rect = character1.to_rect()
    character2_rect = character2.to_rect()

    if rect_in_rect(*(character1_rect + character2_rect)):
        return True

    return False