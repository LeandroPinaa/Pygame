import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, app):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        # isso aqui é pra colocar as 12 animações do pacman, 3 pra cada lado
        self.player_list = list()
        self.cheio = self.app.SpriteSheet.subsurface((487, 0), (16, 16))
        x, y = 455, 0
        for a in range(1, 13):
            if a % 3 == 0:
                self.player_list.append(self.cheio)
                x = 455
                y += 16
            else:
                self.player_list.append(self.app.SpriteSheet.subsurface((x, y), (16, 16)))
                x += 16

        self.current = 0
        self.image = self.player_list[self.current]
        self.image = pg.transform.scale(self.image, (PACMAN_LENGTH, PACMAN_WIDTH))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.app.initial_pos_player[0]*self.app.cell1+25, self.app.initial_pos_player[1]*self.app.cell2+25
        self.mask = pg.sprite.from_surface(self.image)
        self.direction, self.side, self.stored_direction = [0, 0], None, None
        self.correct_pos = self.app.initial_pos_player[:]  # posição correta de acordo com matriz. ex: [13, 29] pacman
        self.lives, self.lives_sprite = 3, self.player_list[4]

    def update(self):
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        self.correct_pos[0] = (self.rect.x - 25)//self.app.cell1
        self.correct_pos[1] = (self.rect.y - 25)//self.app.cell2
        self.animate()
        if self.correct_pos == [-1, 14]:
            self.rect.x, self.rect.y = 27 * self.app.cell1 + 25, 14 * self.app.cell2 + 25
        if self.correct_pos == [28, 14]:
            self.rect.x, self.rect.y = 25, 14 * self.app.cell2 + 25

        self.wall_collision()

        if self.time_to_move():  # hora de mover qnd chega no centro da célula
            if self.stored_direction is not None:
                self.direction = self.stored_direction
        if self.correct_pos in self.app.coins:  # verificar e comer moedas
            self.app.coins.remove(self.correct_pos)
            self.app.score += 1

    def wall_collision(self):  # colisão com a parede
        for wall in self.app.walls:
            if self.rect.colliderect(wall.rect):
                if self.direction[0] > 0:
                    self.rect.right = wall.rect.left
                if self.direction[0] < 0:
                    self.rect.left = wall.rect.right
                if self.direction[1] > 0:
                    self.rect.bottom = wall.rect.top
                if self.direction[1] < 0:
                    self.rect.top = wall.rect.bottom

    def animate(self):
        # animações
        if self.side == 'RIGHT' or self.side is None:
            self.current += 0.25
            list_right = self.player_list[0:3]
            if self.current >= len(list_right):
                self.current = 0
            self.image = list_right[int(self.current)]
            self.image = pg.transform.scale(self.image, (PACMAN_LENGTH, PACMAN_WIDTH))
        elif self.side == 'LEFT':
            self.current += 0.25
            list_left = self.player_list[3:6]
            if self.current >= len(list_left):
                self.current = 0
            self.image = list_left[int(self.current)]
            self.image = pg.transform.scale(self.image, (PACMAN_LENGTH, PACMAN_WIDTH))
        elif self.side == 'UP':
            self.current += 0.25
            list_up = self.player_list[6:9]
            if self.current >= len(list_up):
                self.current = 0
            self.image = list_up[int(self.current)]
            self.image = pg.transform.scale(self.image, (PACMAN_LENGTH, PACMAN_WIDTH))
        elif self.side == 'DOWN':
            self.current += 0.25
            list_down = self.player_list[9:12]
            if self.current >= len(list_down):
                self.current = 0
            self.image = list_down[int(self.current)]
            self.image = pg.transform.scale(self.image, (PACMAN_LENGTH, PACMAN_WIDTH))

    def time_to_move(self):
        if int(self.rect.x-25) % self.app.cell1 == 0:
            if self.direction == [2, 0] or self.direction == [-2, 0] or self.direction == [0, 0]:
                return True
        if int(self.rect.y - 25) % self.app.cell2 == 0:
            if self.direction == [0, 2] or self.direction == [0, -2] or self.direction == [0, 0]:
                return True
        return False


class Wall(pg.sprite.Sprite):
    def __init__(self, app, x, y):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.x, self.y = x, y
        self.app.walls.append(self)
        self.rect = pg.Rect(x*self.app.cell1+25, y*self.app.cell2+25, self.app.cell1, self.app.cell2)
