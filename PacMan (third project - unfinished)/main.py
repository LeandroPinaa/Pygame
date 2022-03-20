import pygame as pg
from settings import *
from player_class import *
from ghost_class import *

pg.init()
pg.mixer.init()


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((LENGTH, WIDTH))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        # proporções da célula/quadrado do meu mapeamento. 20, 20
        self.cell1, self.cell2 = MAZE_LENGTH // 28, MAZE_WIDTH // 30
        # atributos de estado do jogo
        self.running, self.playing, self.waiting = True, False, False
        # setando os atributos de arquivo none pra chamar o método e arrumar eles lá, como tb lista walls e coins
        self.logo, self.SpriteSheet, self.maze = None, None, None
        self.initial_pos_player = None  # pos inicial player
        self.walls, self.coins, self.score = [], [], 0
        self.group = pg.sprite.Group()
        self.load()
        # atributo player/ghost é um objeto q contém toda sua classe. atributo grupo vai conter todas as sprites
        self.player = Player(self)
        self.group.add(self.player)

# ======================================== IN-GAME METHODS =============================================================

    def in_game(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.player.stored_direction = [-2, 0]
                    self.player.side = 'LEFT'
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.player.stored_direction = [2, 0]
                    self.player.side = 'RIGHT'
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.player.stored_direction = [0, -2]
                    self.player.side = 'UP'
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.player.stored_direction = [0, 2]
                    self.player.side = 'DOWN'

    def update(self):
        pg.display.flip()
        self.group.update()

    def draw(self):
        self.screen.fill(BLACK)
        maze_rect = self.maze.get_rect()
        maze_rect.center = LENGTH//2, WIDTH//2
        self.screen.blit(self.maze, maze_rect)
        # self.grid()
        self.show_message(f'CURRENT SCORE: {self.score}', 25, GREEN, 150, 5)
        for coin in self.coins:
            pg.draw.circle(self.screen, GRAY, (coin[0]*self.cell1+36, coin[1]*self.cell2+36), 3)
        self.group.draw(self.screen)
        for live in range(self.player.lives):
            self.screen.blit(self.player.lives_sprite, (50+25*live, 650))

# =========================================== HELP METHODS =============================================================

    def show_message(self, msg, size, color, x, y):
        font = pg.font.SysFont(FONT, size, True)
        formatted_text = font.render(msg, True, color)
        formatted_text_rect = formatted_text.get_rect()
        formatted_text_rect.midtop = (x, y)
        self.screen.blit(formatted_text, formatted_text_rect)

    def load(self):
        # carregar música e arquivos png, wav, txt, labirinto
        pg.mixer.music.load(START_SCREEN_SONG)
        pg.mixer.music.set_volume(0.3)
        self.logo = pg.image.load(PACMAN_LOGO).convert_alpha()
        self.SpriteSheet = pg.image.load(SPRITE_SHEET).convert_alpha()
        self.maze = self.SpriteSheet.subsurface((228, 0), (225, 248))
        self.maze = pg.transform.scale(self.maze, (MAZE_LENGTH, MAZE_WIDTH))
        with open('walls.txt', 'r') as file:
            number = 1
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == '1':
                        Wall(self, x, y)
                    if char == 'c':
                        self.coins.append([x, y])
                    if char == 'P':
                        initial_pos_player = [x, y]
                        self.initial_pos_player = initial_pos_player
                    if char == 'G':
                        self.group.add(Ghost(self, number, x, y))
                        number += 1

    def grid(self):
        # linha e coluna traçadas na tela pra mapear
        border1, border2 = (LENGTH-MAZE_LENGTH)//2, (WIDTH-MAZE_WIDTH)//2
        for x in range(self.cell1+12):
            pg.draw.line(self.screen, GRAY, (border1, border2+x*self.cell1), (MAZE_LENGTH+border1, border2+x*self.cell1), 2)
        for x in range(self.cell2+9):
            pg.draw.line(self.screen, GRAY, (border1+x*self.cell2, border2), (border1+x*self.cell2, MAZE_WIDTH+border2), 2)

# =================================== START AND GAME OVER SCREEN =======================================================

    def start_screen(self):
        self.screen.fill(BLACK)
        logo_rect = self.logo.get_rect()
        logo_rect.midtop = (LENGTH//2, 40)
        self.screen.blit(self.logo, logo_rect)
        self.show_message('-PRESS BACKSPACE TO START', 25, LIGHT_BLUE, LENGTH//2, WIDTH//2+30)
        self.show_message('@Developed by Leandro Pina', 20, WHITE, LENGTH//2, WIDTH-25)
        pg.mixer.music.play(-1)
        self.waiting = True
        pg.display.flip()  # como dentro do while n muda nada na tela posso deixar o flip aqui
        while self.waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running, self.waiting = False, False
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.waiting = False
                    pg.mixer.music.stop()
                    pg.mixer.Sound(MUNCH_SOUND).play()

    def game_over_screen(self):
        pass


game = Game()
game.start_screen()
while game.running:
    game.in_game()
    game.game_over_screen()
