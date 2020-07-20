import pygame
import os
import time
import random
import ctypes
import copy

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conga")
WRONG_CLICK = False

LINE_AD_X = 0.35
LINE_AD_Y = 0.2

HUMAN = 'White'
AI = 'Black'

PLAYER_COLOR = {
    'White': (250, 250, 250),
    'Black': (0, 0, 0)
}

CURRENT_PLAYER = HUMAN

SCORE = {
    AI: 1000,
    HUMAN: -1000,
    "White_FIVE_STONES_BLOCKED": 5,
    "Black_FIVE_STONES_BLOCKED": -5,
    "White_THREE_STONES_BLOCKED": 3,
    "Black_THREE_STONES_BLOCKED": -3,
    "White_ONE_STONE_BLOCKED": 1,
    "Black_ONE_STONE_BLOCKED": -1,
}

DIRECTIONS = {
    "UP": [(lambda i, k: i-k), (lambda j, k: j)],
    "UPRIGHT": [(lambda i, k: i-k), (lambda j, k: j+k)],
    "RIGHT": [(lambda i, k: i), (lambda j, k: j+k)],
    "DOWNRIGHT": [(lambda i, k: i+k), (lambda j, k: j+k)],
    "DOWN": [(lambda i, k: i+k), (lambda j, k: j)],
    "DOWNLEFT": [(lambda i, k: i+k), (lambda j, k: j-k)],
    "LEFT": [(lambda i, k: i), (lambda j, k: j-k)],
    "UPLEFT": [(lambda i, k: i-k), (lambda j, k: j-k)]
}


def mark_placement_pos_find(left, right, top, bottom):
    x = (right - left)/2
    y = (bottom - top)/2
    offset = x/5
    return (left + x-offset, top + y-offset)


def color_coord(left, right, top, bottom):
    return (left, top, right-left, bottom-top)


ENTRY_POS = {1: mark_placement_pos_find(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
             2: mark_placement_pos_find(WIDTH * LINE_AD_X, int(WIDTH/2), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
             3: mark_placement_pos_find(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
             4: mark_placement_pos_find(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
             5: mark_placement_pos_find(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*LINE_AD_X, int(HEIGHT/2)),
             6: mark_placement_pos_find(WIDTH * LINE_AD_X, int(WIDTH/2), HEIGHT*LINE_AD_X, int(HEIGHT/2)),
             7: mark_placement_pos_find(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), HEIGHT*LINE_AD_X, int(HEIGHT/2)),
             8: mark_placement_pos_find(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*LINE_AD_X, int(HEIGHT/2)),
             9: mark_placement_pos_find(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
             10: mark_placement_pos_find(WIDTH * LINE_AD_X, int(WIDTH/2), int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
             11: mark_placement_pos_find(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
             12: mark_placement_pos_find(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
             13: mark_placement_pos_find(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
             14: mark_placement_pos_find(WIDTH * LINE_AD_X, int(WIDTH/2), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
             15: mark_placement_pos_find(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
             16: mark_placement_pos_find(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y))
             }

COLOR_BOX_COORD = {1: color_coord(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
                   2: color_coord(WIDTH * LINE_AD_X, int(WIDTH/2), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
                   3: color_coord(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
                   4: color_coord(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
                   5: color_coord(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*LINE_AD_X, int(HEIGHT/2)),
                   6: color_coord(WIDTH * LINE_AD_X, int(WIDTH/2), HEIGHT*LINE_AD_X, int(HEIGHT/2)),
                   7: color_coord(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), HEIGHT*LINE_AD_X, int(HEIGHT/2)),
                   8: color_coord(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*LINE_AD_X, int(HEIGHT/2)),
                   9: color_coord(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
                   10: color_coord(WIDTH * LINE_AD_X, int(WIDTH/2), int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
                   11: color_coord(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
                   12: color_coord(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), int(HEIGHT/2), HEIGHT*(1 - LINE_AD_X)),
                   13: color_coord(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
                   14: color_coord(WIDTH * LINE_AD_X, int(WIDTH/2), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
                   15: color_coord(int(WIDTH/2), WIDTH * (1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
                   16: color_coord(WIDTH*(1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y))
                   }
