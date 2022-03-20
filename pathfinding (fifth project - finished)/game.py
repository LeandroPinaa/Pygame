import pygame as pg
from pygame.math import Vector2 as vec
from pygame.locals import *
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class Pathfinder:
    def __init__(self, matrix):
        # main setup
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.selection_surf = pg.image.load('Pathfinding Project/selection.png').convert_alpha()
        # pathfinding
        self.path = []
        # roomba
        self.roomba = pg.sprite.GroupSingle(Roomba(self.empty_path))  # como só vou botar uma sprite no grupo uso single

    def empty_path(self):  # when roomba reached end, we empty the self.path (not very necessary, but it's fine)
        self.path = []

    def draw_active_cell(self):
        mouse_pos = pg.mouse.get_pos()
        row = mouse_pos[1] // 32
        col = mouse_pos[0] // 32
        if self.matrix[row][col] == 1:
            rect = pg.Rect((col * 32, row * 32), (32, 32))
            screen.blit(self.selection_surf, rect)

    def create_path(self):
        # start
        start_x, start_y = self.roomba.sprite.get_coord()
        start = self.grid.node(start_x, start_y)

        # end
        mouse_pos = pg.mouse.get_pos()
        end_x, end_y = mouse_pos[0] // 32, mouse_pos[1] // 32
        end = self.grid.node(end_x, end_y)

        # path
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()  # precisa limpar o grid pq, a variável start, quando roda o finder.find_path, se torna
        # igual ao end, ficando start=end. Como nesse projeto a cada click a gente quer diferente, pode limpar
        self.roomba.sprite.set_path(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                points.append((x, y))
            pg.draw.lines(screen, '#4a4a4a', False, points, 5)

    def update(self):
        self.draw_active_cell()
        self.draw_path()

        # roomba updating and drawing
        self.roomba.update()
        self.roomba.draw(screen)


class Roomba(pg.sprite.Sprite):
    def __init__(self, empty_path):
        super().__init__()
        self.image = pg.image.load('Pathfinding Project/roomba.png').convert_alpha()
        self.rect = self.image.get_rect(center=(60, 60))

        # movement
        self.pos = self.rect.center
        self.speed = 3
        self.direction = vec(0, 0)

        # path
        self.path = []
        self.collision_rects = []
        self.empty_path = empty_path

    def get_coord(self):
        col = self.rect.centerx // 32
        row = self.rect.centery // 32
        return col, row

    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                rect = pg.Rect((x - 2, y - 2), (4, 4))
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = vec(self.pos)
            end = vec(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = vec(0, 0)
            self.path = []

    def check_collision(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.empty_path()

    def update(self):
        # obs: a razão de usar esse pos como movimento ao invés do self.rect.center direto é pq pygame n é mto
        # compatível com coordenadas e vectors, ent fica melhor assim
        self.pos += self.direction * self.speed
        self.check_collision()
        self.rect.center = self.pos


# pygame setup
pg.init()
screen = pg.display.set_mode((1280, 736))
clock = pg.time.Clock()

# game setup
bg_surf = pg.image.load('Pathfinding Project/map.png').convert_alpha()
matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
     0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1,
     1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1,
     1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0,
     0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0,
     0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1,
     1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1,
     1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0]]
pathfinder = Pathfinder(matrix)

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:  # when we click
            pathfinder.create_path()
    screen.blit(bg_surf, (0, 0))
    pathfinder.update()

    pg.display.flip()
    clock.tick(60)
