import pygame as pg
from settings import *
from debug import debug
from level import Level

# a classe Game conterá os métodos principais para rodar o game, como também o objeto Level
# OBS: única diferença atualmente do meu código pro do clear code é que eu n utillizei o hitbox no inflate, mas sim rect
# OBS: outra diferença é que o meu create_weapon e destroy_weapon são os create_attack e destroy_attack do cara
# OBS: outra diferença é que meu magic e weapon overlay eu fiz bem diferente do dele (no caso o meu melhor EZ CLAP)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_m:
                        self.level.toggle_menu()
            self.screen.fill(WATER_COLOR)
            self.level.run(self.clock)

            pg.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
