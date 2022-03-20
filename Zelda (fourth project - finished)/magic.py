import pygame as pg
from settings import *
from pygame.math import Vector2 as vec
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            magic_sound = pg.mixer.Sound(MAGIC_DATA['heal']['sound'])
            magic_sound.set_volume(0.8)
            magic_sound.play()
            player.health += strength
            player.energy -= cost
            if player.health > player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('heal', player.rect.center + vec(0, -50), groups)
            self.animation_player.create_particles('aura', player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            magic_sound = pg.mixer.Sound(MAGIC_DATA['flame']['sound'])
            magic_sound.set_volume(0.3)
            magic_sound.play()
            player.energy -= cost
            if player.status.split('_')[0] == 'right':
                direction = vec(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = vec(-1, 0)
            elif player.status.split('_')[0] == 'down':
                direction = vec(0, 1)
            else:
                direction = vec(0, -1)

            for i in range(1, 6):
                if direction[0]:
                    offset_x = (direction[0] * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + randint(-TILESIZE//3, TILESIZE//3)  # o randint é pra deixar menos reto
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:
                    offset_y = (direction[1] * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame', (x, y), groups)
