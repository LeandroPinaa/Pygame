import pygame as pg
from settings import *

pg.init()
font = pg.font.SysFont(None, 30)


def debug(info, x=10, y=10):
    display_surf = pg.display.get_surface()
    debug_surf = font.render(str(info), True, WHITE)
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pg.draw.rect(display_surf, BLACK, debug_rect)
    display_surf.blit(debug_surf, debug_rect)
