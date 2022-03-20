import pygame as pg
from settings import *
from pygame.math import Vector2 as vec


class Weapon(pg.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.player_direction = player.status.split('_')[0]
        # graphics
        full_path = f'graphics/weapons/{player.weapon}/{self.player_direction}.png'
        self.image = pg.image.load(full_path).convert_alpha()
        # placement of the weapon
        if self.player_direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + vec(0, 16))
        elif self.player_direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + vec(0, 16))
        elif self.player_direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + vec(-10, 0))
        else:
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + vec(-10, 0))
