import pygame as pg
from settings import *
from pygame.math import Vector2 as vec
from math import sin

# classe sprite q será a herdada da classe player e enemy, pq ambos tem quase as mesmas coisas


class Entity(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.hitbox = None
        self.current = 0
        self.direction = vec(0, 0)
        self.value = None

    def move(self, speed):
        if self.direction.magnitude() != 0:  # verificar se o direction n está vazio: (0, 0)
            self.direction = self.direction.normalize()  # normalizar a direção, pq na diagonal fica um pouco + rápido
        self.hitbox.x += self.direction[0] * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction[1] * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction[0] > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction[0] < 0:
                        self.hitbox.left = sprite.hitbox.right
        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction[1] > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction[1] < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        self.value = sin(pg.time.get_ticks())
        if self.value >= 0:
            return 255
        else:
            return 0
