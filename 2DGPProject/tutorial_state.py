import game_framework
import map_loader
import collision

import character_data
import finn_character
import cubchoo_character
import terrorlight_character

import maple_particle
import snow_particle
import cloud_particle

import effect_handler
import warp_effect
import damage_effect
import push_effect

import title_state
import tutorial_state
import game_state_level_01

from pico2d import *
from pico2d_extension import *


name = "Tutorial"


def enter():

    global game_play, game_clear
    game_play = True
    game_clear = False

    global background_music, game_clear_music 
    background_music = load_music('Resources/Musics/GameState.ogg')
    background_music.set_volume(64)
    background_music.repeat_play()

    game_clear_music = load_music('Resources/Musics/GameClear.ogg')
    game_clear_music.set_volume(64)

    global background_image
    background_image = load_image('Resources/States/Background_01.png')

    global background_gameclear
    background_gameclear = load_image('Resources/States/GameClearState.png')

    global back_image
    back_image = load_image('Resources/Images/Back.png')

    global next_image
    next_image = load_image('Resources/Images/Next.png')

    global map
    map = map_loader.load_map('Resources/Maps/Tutorial.json')
    
    global finn
    finn = finn_character.Finn()
    start = map.to_trigger('Start')
    finn.x, finn.y = start.x, map.mapoffsety + map.mapheight - start.y

    global effects
    effects = effect_handler.EffectHandler()

    global cubchooes, cubchoo_respone_time, cubchoo_respone_start
    cubchooes = []
    cubchoo_respone_time = 0.0
    cubchoo_respone_start = False

    global terrorlights, terrorlight_respone_time_A, terrorlight_respone_time_B, terrorlight_respone_start
    terrorlights = []
    terrorlight_respone_time_A = 0.0
    terrorlight_respone_time_B = 0.0
    terrorlight_respone_start = False

    global maples
    maples = [maple_particle.Maple() for i in range(30)]
    '''
    global snows
    snows = [snow_particle.Snow() for i in range(50)]
    '''
    global clouds
    clouds = [cloud_particle.Cloud() for i in range(10)]

    global tutorial_font, tutorial_str
    tutorial_font = load_font('Resources/Fonts/NanumBarunGothicBold.TTF', 12)
    tutorial_str = ''


def exit():
    global background_music, game_clear_music
    del (background_music)
    del (game_clear_music)
    
    global background_image, back_image, next_image
    del (background_image)
    del (back_image)
    del (next_image)
    global map
    del (map)

    global background_gameclear
    del (background_gameclear)

    global effects
    del (effects)
    
    global cubchooes, cubchoo_respone_time, cubchoo_respone_start
    del (cubchooes)
    del (cubchoo_respone_time)
    del (cubchoo_respone_start)

    global terrorlights, terrorlight_respone_time_A, terrorlight_respone_time_B, terrorlight_respone_start
    
    del (terrorlights)
    del (terrorlight_respone_time_A)
    del (terrorlight_respone_time_B)
    del (terrorlight_respone_start)

    global game_play, game_clear
    del (game_play)
    del (game_clear)


    global maples, snows, clouds
    del(maples)
    #del(snows)
    del(clouds)

    global tutorial_font, tutorial_str
    del (tutorial_font)
    del (tutorial_str)


def update(frame_time):

    global game_play, game_clear
    if not game_play:
        return

    if finn.life:
        finn.update(frame_time)
        collision.collision_tile_and_character(map, finn, frame_time)
        collision.collision_object_and_character(map, finn, frame_time)
    else:
        game_framework.change_state(tutorial_state)


    for terrorlight in terrorlights:
        terrorlight.update(frame_time)
        
        if collision.collision_player_and_character(finn, terrorlight):
            effect_x = min(finn.x, terrorlight.x) + abs(finn.x - terrorlight.x) // 2
            effect_y = min(finn.y, terrorlight.y) + abs(finn.y - terrorlight.y) // 2
            effects.add_effect(damage_effect.DamageEffect(effect_x, effect_y))
            finn.play_hit_sound()
            if finn.speed > 30:
                finn.speed -= 10
                
        collision.collision_map_and_character(map, terrorlight, frame_time) 
        collision.collision_object_and_character(map, terrorlight, frame_time)
    
    global terrorlight_respone_start
    if terrorlight_respone_start and len(terrorlights) <= 4:
        global terrorlight_respone_time_A, terrorlight_respone_time_B
        terrorlight_respone_time_A -= frame_time
        terrorlight_respone_time_B -= frame_time
        if terrorlight_respone_time_A < 0:
            object = map.to_trigger('Respone-C')
            terrorlight = terrorlight_character.Terrorlight()
            terrorlight.x, terrorlight.y = object.x, map.mapoffsety + map.mapheight - object.y
            terrorlights.append(terrorlight)
            terrorlight_respone_time_A = 3.0
        elif terrorlight_respone_time_B < 0:
            object = map.to_trigger('Respone-B')
            terrorlight = terrorlight_character.Terrorlight()
            terrorlight.x, terrorlight.y = object.x, map.mapoffsety + map.mapheight - object.y
            terrorlights.append(terrorlight)
            terrorlight_respone_time_B = 3.0
    

    for cubchoo in cubchooes:
        cubchoo.update(frame_time) 
        
        if finn.frame_stop:
            if collision.collision_player_and_character(finn, cubchoo):
                effect_x = min(finn.x, cubchoo.x) + abs(finn.x - cubchoo.x) // 2
                effect_y = min(finn.y, cubchoo.y) + abs(finn.y - cubchoo.y) // 2
                effects.add_effect(damage_effect.DamageEffect(effect_x, effect_y))
                finn.play_hit_sound()
        else:
            if collision.collision_player_and_character(cubchoo, finn):
                effect_x = min(finn.x, cubchoo.x) + abs(finn.x - cubchoo.x) // 2
                effect_y = min(finn.y, cubchoo.y) + abs(finn.y - cubchoo.y) // 2
                effects.add_effect(push_effect.PushEffect(effect_x, effect_y))
                cubchoo_character.Cubchoo.hit_sound.play()
                finn.frame_stop = True
                
        collision.collision_object_and_character(map, cubchoo, frame_time) 
        collision.collision_tile_and_character(map, cubchoo, frame_time)
        if cubchoo.opacify < 0:
            cubchooes.remove(cubchoo)
    
    global cubchoo_respone_start
    if cubchoo_respone_start:
        if len(cubchooes) <= 10:
            global cubchoo_respone_time
            cubchoo_respone_time -= frame_time
            if cubchoo_respone_time < 0:
                object = map.to_trigger('Respone-A')
                cubchoo = cubchoo_character.Cubchoo()
                cubchoo.x, cubchoo.y = object.x, map.mapoffsety + map.mapheight - object.y
                cubchooes.append(cubchoo)
                cubchoo_character.Cubchoo.respone_sound.play()
                cubchoo_respone_time = 1.0

    
    effects.update(frame_time)

    map.update(finn, frame_time)

    for maple in maples:
        maple.update(frame_time)

    '''
    for snow in snows:
        snow.update(frame_time)
    '''

    for cloud in clouds:
        cloud.update(frame_time)

    collision_trigger_and_player()


def draw(frame_time):
    
    clear_canvas()

    background_image.draw(game_framework.width//2, game_framework.height//2)

    map.draw_ground()
    if game_framework.debug:
        map.draw_hexagon_on_point(finn.x, finn.y)
   
    if finn.life:
        finn.draw()
   
    for cubchoo in cubchooes:
        cubchoo.draw()

    for terrorlight in terrorlights:
        terrorlight.draw()
   
    map.draw_object()

    effects.draw()

    for maple in maples:
        maple.draw()
    '''
    for snow in snows:
        snow.draw()
    '''
    for cloud in clouds:
        cloud.draw()

    global tutorial_font, tutorial_str
    tutorial_font.draw(finn.x, finn.y + 50, tutorial_str, (255, 255, 255))

    if game_play:
        next_image.draw(game_framework.width - next_image.w // 2 - 10, game_framework.height - next_image.h // 2 - 10)
        back_image.draw(back_image.w // 2 + 10, game_framework.height - back_image.h // 2 - 10)
    elif game_clear:
        background_gameclear.draw(game_framework.width//2, game_framework.height//2)
        back_image.draw (game_framework.width // 2 - back_image.w, game_framework.height // 5 + back_image.h // 2)
        next_image.draw(game_framework.width  // 2 + next_image.w, game_framework.height // 5 + next_image.h // 2)

    update_canvas()


def handle_events(frame_time):

    global game_play, game_clear
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            state = finn.get_state_from_key(event.key)
            if state is not None:
                finn.change_state(state)
           
        elif event.type == SDL_KEYUP:
            if event.key == finn.get_key_from_state():
                finn.frame_stop = True

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if game_play:
                if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                       game_framework.width - next_image.w // 2 - 10, game_framework.height - next_image.h // 2 - 10,
                                        next_image.w, next_image.h):
                    game_framework.change_state(game_state_level_01)
                    return;
                elif collision.point_in_rect(event.x, game_framework.height - event.y, \
                                    back_image.w // 2 + 10, game_framework.height - back_image.h // 2 - 10,
                                    back_image.w, back_image.h):
                    game_framework.change_state(title_state)
                    return;
            elif game_clear:
                if collision.point_in_rect(event.x, game_framework.height - event.y, \
                                       game_framework.width // 2 - back_image.w, game_framework.height // 5 + back_image.h // 2,
                                        back_image.w, back_image.h):
                    game_framework.change_state(title_state)
                    return;
                elif collision.point_in_rect(event.x, game_framework.height - event.y, \
                                       game_framework.width // 2 + next_image.w, game_framework.height // 5 + next_image.h // 2,
                                        next_image.w, next_image.h):
                    game_framework.change_state(game_state_level_01)
                    return;


def pause():
    pass


def resume():
    pass


def collision_trigger_and_player():

    global tutorial_str
    global cubchooes, cubchoo_respone_start

    for object in map.trigger_layer.objects:

        object_rect = map.to_object_rect(object)
        player_rect = finn.to_rect()

        if object.name == 'Warp-A':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                effects.add_effect(warp_effect.WarpEffect(finn.x, finn.y))
                        
                portalB = map.to_trigger('Warp-B')
                portalB_rect = map.to_object_rect(portalB)
                effects.add_effect(warp_effect.WarpEffect(portalB_rect[0], portalB_rect[1]))
                finn.x, finn.y = portalB_rect[0], portalB_rect[1]

                warp_effect.WarpEffect.sound.play()

        if object.name == 'Warp-C':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                effects.add_effect(warp_effect.WarpEffect(finn.x, finn.y))
                        
                portalD = map.to_trigger('Warp-D')
                portalD_rect = map.to_object_rect(portalD)
                effects.add_effect(warp_effect.WarpEffect(portalD_rect[0], portalD_rect[1]))
                finn.x, finn.y = portalD_rect[0], portalD_rect[1]

                warp_effect.WarpEffect.sound.play()

                cubchoo_respone_start = False
                cubchooes.clear()
                global terrorlight_respone_start
                terrorlight_respone_start = True

                tutorial_str = '거의 다 왔어!'


        elif object.name == 'Home':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                global game_play, game_clear
                game_play = False
                game_clear = True
                background_music.stop()
                game_clear_music.repeat_play()


        elif object.name == 'Tutorial-0':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = "방향키로 날 움직여봐!"


        elif object.name == 'Tutorial-1':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '이제부터 블록이 점점 사라질꺼야!'


        elif object.name == 'Tutorial-2':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '지형물이 있는 블록은 사라지지 않아!'


        elif object.name == 'Tutorial-2-1':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '지형물을 잘 이용하면 좋을거 같애!'


        elif object.name == 'Tutorial-3':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '회색 블록까지 가보자!'


        elif object.name == 'Tutorial-4':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '회색 블록에 가면 순간이동해!'


        elif object.name == 'Tutorial-5':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '몬스터다! 부딪히지않게 조심해!'
                cubchoo_respone_start = True


        elif object.name == 'Tutorial-6':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '몬스터를 만나면, 방향키로 연타해서 밀어버리자!'


        elif object.name == 'Tutorial-7':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '날아다니는 몬스터를 피해서 지나가자!'

        elif object.name == 'Tutorial-8':
            if collision.rect_in_rect(*(player_rect + object_rect)):
                tutorial_str = '얼른 집으로 가자!'
