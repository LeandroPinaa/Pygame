import pygame as pg
from settings import *
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Ghost(pg.sprite.Sprite):
    def __init__(self, app, number, x, y):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.number = number
        self.current = 0
        if number == 1:
            self.type, self.red_list = 'RED', []
            for a in range(455, 456 + (16 * 7), 16):
                self.red_list.append(self.app.SpriteSheet.subsurface((a, 64), (16, 16)))
            self.image = self.red_list[self.current]
        elif number == 2:
            self.type, self.pink_list = 'PINK', []
            for a in range(455, 456 + (16 * 7), 16):
                self.pink_list.append(self.app.SpriteSheet.subsurface((a, 80), (16, 16)))
            self.image = self.pink_list[self.current]
        elif number == 3:
            self.type, self.lightblue_list = 'LIGHTBLUE', []
            for a in range(455, 456 + (16 * 7), 16):
                self.lightblue_list.append(self.app.SpriteSheet.subsurface((a, 96), (16, 16)))
            self.image = self.lightblue_list[self.current]
        elif number == 4:
            self.type, self.orange_list = 'ORANGE', []
            for a in range(455, 456 + (16 * 7), 16):
                self.orange_list.append(self.app.SpriteSheet.subsurface((a, 112), (16, 16)))
            self.image = self.orange_list[self.current]

        self.image = pg.transform.scale(self.image, (GHOST_LENGTH, GHOST_WIDTH))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * self.app.cell1 + 25, y * self.app.cell2 + 25
        self.mask = pg.sprite.from_surface(self.image)
        self.initial_pos_ghost = [x, y]
        self.correct_pos = self.initial_pos_ghost[:]
        self.direction = [0, 0]
        self.sla = True

    def update(self):
        if self.type == 'RED':
            self.red_animate()

            target = self.app.player.correct_pos  # pacman = [13, 29]
            start = self.correct_pos  # do red = [11, 13]

    def wall_collision(self):
        for wall in self.app.walls:  # colisão com a parede
            if self.rect.colliderect(wall.rect):
                if self.direction[0] > 0:
                    self.rect.right = wall.rect.left
                    return True
                if self.direction[0] < 0:
                    self.rect.left = wall.rect.right
                    return True
                if self.direction[1] > 0:
                    self.rect.bottom = wall.rect.top
                    return True
                if self.direction[1] < 0:
                    self.rect.top = wall.rect.bottom
                    return True
            return False

    def red_animate(self):
        if self.direction == [1, 0] or self.direction == [0, 0]:
            self.current += 0.25
            list_right = self.red_list[0:2]
            if self.current >= len(list_right):
                self.current = 0
            self.image = list_right[int(self.current)]
            self.image = pg.transform.scale(self.image, (GHOST_LENGTH, GHOST_WIDTH))
        elif self.direction == [-1, 0]:
            self.current += 0.25
            list_left = self.red_list[2:4]
            if self.current >= len(list_left):
                self.current = 0
            self.image = list_left[int(self.current)]
            self.image = pg.transform.scale(self.image, (GHOST_LENGTH, GHOST_WIDTH))
        elif self.direction == [0, -1]:
            self.current += 0.25
            list_up = self.red_list[4:6]
            if self.current >= len(list_up):
                self.current = 0
            self.image = list_up[int(self.current)]
            self.image = pg.transform.scale(self.image, (GHOST_LENGTH, GHOST_WIDTH))
        elif self.direction == [0, 1]:
            self.current += 0.25
            list_down = self.red_list[6:8]
            if self.current >= len(list_down):
                self.current = 0
            self.image = list_down[int(self.current)]
            self.image = pg.transform.scale(self.image, (GHOST_LENGTH, GHOST_WIDTH))

    def pink_animate(self):
        pass

    def lightblue_animate(self):
        pass

    def orange_animate(self):
        pass
