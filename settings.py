import pygame as pg
import sys

vec2 = pg.math.Vector2

RES = WIDTH, HEIGHT = vec2(1600, 900)
# RES = WIDTH, HEIGHT = vec2(1920, 1080)
CENTER = H_WIDTH, H_HEIGHT = RES // 2
TILE_SIZE = 250  #

PLAYER_SPEED = 0.4
PLAYER_ROT_SPEED = 0.0015

BG_COLOR = '#117c13'  #
NUM_ANGLES = 72  # multiple of 360 -> 24, 30, 36, 40, 45, 60, 72, 90, 120, 180

# entity settings
ENTITY_SPRITE_ATTRS = {
    'player': {
        'path': 'assets/entities/player/SegrtHugo-novo.png',
        'mask_path': 'assets/entities/player/mask.png', 
        'num_layers': 5,
        'scale': 3,
        'y_offset': 0,
    },
    'explosion': {
        'num_layers': 7,
        'scale': 1.0,
        'path': 'assets/entities/explosion/explosion.png',
        'y_offset': 50,
    },
    'bullet': {
        'num_layers': 1,
        'scale': 0.4,
        'path': 'assets/entities/bullet/bullet.png',
        'y_offset': 50,
    },
    'MajstorIvan':{
        'num_layers': 9,
        'scale': 3.5,
        'path': 'assets/entities/npcs/MajstorIvan-novo.png',
        'y_offset': 20
    },
    'SeljankaMara':{
        'num_layers': 9,
        'scale': 3,
        'path': 'assets/entities/cats/BabaMilka-novo.png',
        'y_offset': 4
    },
    'MajstorMarko':{
        'num_layers': 1,
        'scale': 3,
        'path': 'assets/entities/cats/MajstorIvan.png',
        'y_offset': 20
    },
    'MajstorDalibor':{
        'num_layers': 1,
        'scale': 3,
        'path': 'assets/entities/cats/MajstorIvan.png',
        'y_offset': 20
    },
    'MajstorLuka':{
        'num_layers': 1,
        'scale': 3,
        'path': 'assets/entities/cats/MajstorIvan.png',
        'y_offset': 20
    },
    'MajstorJanko':{
        'num_layers': 1,
        'scale': 3,
        'path': 'assets/entities/cats/MajstorIvan.png',
        'y_offset': 20
    },
        'jez':{
        'path': 'assets/stacked_sprites/hedgehog.png',
        'num_layers': 2,
        'scale': 3,
        'y_offset': 0,
        'mask_layer': 1
    }
}

# stacked sprites settings
'''mask_layer - index of the layer from which we get the mask for collisions 
and is also cached for all angles of the object, set manually or by default 
equal to num_layer // 2'''

STACKED_SPRITE_ATTRS = {
    'grass': {
        'path': 'assets/stacked_sprites/grass.png',
        'num_layers': 11,
        'scale': 7,
        'y_offset': 20,
        'outline': False,
    },
    'blue_tree': {
        'path': 'assets/stacked_sprites/blue_tree.png',
        'num_layers': 43,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 21,
    },
        'anvil': {
        'path': 'assets/stacked_sprites/anvil.png',
        'num_layers': 28,
        'scale': 4,
        'y_offset': -30,
        'mask_layer': 14
    },
        'chest': {
        'path': 'assets/stacked_sprites/chest.png',
        'num_layers': 20,
        'scale': 3,
        'y_offset': 0,
        'mask_layer': 10
    },
        'bunar': {
        'path': 'assets/stacked_sprites/bunar.png',
        'num_layers': 81,
        'scale': 2.5,
        'y_offset': 0,
        'mask_layer': 40 
    },
        'drvo': {
        'path': 'assets/stacked_sprites/drvo_1.png',
        'num_layers': 80,
        'scale': 3,
        'y_offset': 0,
        'transparency': True,
        'mask_layer': 40
    },
        'breza': {
        'path': 'assets/stacked_sprites/breza.png',
        'num_layers': 80,
        'scale': 5,
        'y_offset': 0,
        'transparency': True,
        'mask_layer': 40
    },
        'stol_majstor':{
        'path': 'assets/stacked_sprites/stol_majstor.png',
        'num_layers': 19,
        'scale': 3,
        'y_offset': 0,
        'mask_layer': 9
    },
        'crafting':{
        'path': 'assets/stacked_sprites/crafting_table.png',
        'num_layers': 16,
        'scale': 4,
        'y_offset': 0,
        'mask_layer': 8
    },
        'radni_stol':{
        'path': 'assets/stacked_sprites/radni_stol_Hugo.png',
        'num_layers': 72,
        'scale': 2,
        'y_offset': 0,
        'mask_layer': 34
    }
}


















