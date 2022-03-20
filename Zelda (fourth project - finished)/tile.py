import pygame as pg
from settings import *

# classe do tile/cell/célula/quadrado do mapa, por exemplo as rochas q estarão em cada tile como obstáculo
from pygame.sprite import AbstractGroup


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pg.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type  # se vai ser rocha, inimigo, etc
        # abaixo é pq cada imagem vai ter vários tamanhos diferentes como grama e árvore, porém caso eu n mande nada
        self.image = surface  # de parâmetro, o tamanho fica como (64, 64), que é o padrão tilesize
        if self.sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
            self.hitbox = self.rect.inflate(0, -50)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -10)
        # abaixo o inflate muda o tamanho do retângulo, como eu n quero mudar o lado direito nem esquerdo, eu deixo x=0,
        # porém pro y eu deixo por exemplo = -10, ou seja, encolhe 5 pixels cima e em baixo.
