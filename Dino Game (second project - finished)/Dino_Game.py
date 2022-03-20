import pygame as pg
from pygame.locals import *
from random import randrange, choice

pg.init()
pg.mixer.init()
death = pg.mixer.Sound('sons_death_sound.wav')
jump = pg.mixer.Sound('sons_jump_sound.wav')
score = pg.mixer.Sound('sons_score_sound.wav')
length, width = 640, 480
tela = pg.display.set_mode((length, width))
pg.display.set_caption('Dino Game')
clock = pg.time.Clock()
SpriteSheet = pg.image.load('dinoSpritesheet.png').convert_alpha()
colidiu,escolha_obstaculo,pontos,velocidade = False,choice([0,1]),0,10


def exibe_mensagem(msg, tamanho, cor):
    fonte = pg.font.SysFont('comicsansms', tamanho, bold=True, italic=False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado


def restart_game():
    global colidiu,escolha_obstaculo,pontos,velocidade
    colidiu,escolha_obstaculo,pontos,velocidade = False, choice([0, 1]), 0, 10
    cactus.rect.x, dino_voador.rect.x = length, length
    dino.rect.center = 100, width - 64
    dino.pulo = False


class Dino(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.dino_list = []
        for a in range(0, 65, 32):
            self.dino_list.append(SpriteSheet.subsurface((a, 0), (32, 32)))
        self.atual = 0
        self.image = self.dino_list[self.atual]
        self.image = pg.transform.scale(self.image, [32 * 3, 32 * 3])
        self.rect = self.image.get_rect()
        self.rect.center = 100, width - 64
        self.mask = pg.sprite.from_surface(self.image)
        self.pulo = False

    def update(self):
        if self.pulo:
            if self.rect.y <= 240:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.center != (100, width - 64):
                self.rect.y += 20

        self.atual += 0.25
        if self.atual >= len(self.dino_list):
            self.atual = 0
        self.image = self.dino_list[int(self.atual)]
        self.image = pg.transform.scale(self.image, [32 * 3, 32 * 3])

    def pular(self):
        if self.rect.center == (100, width - 64):
            self.pulo = True
            jump.play()


class Clouds(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = SpriteSheet.subsurface((224, 0), (32, 32))
        self.image = pg.transform.scale(self.image, [32 * 3, 32 * 3])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randrange(30, 300, 90), randrange(30, 180, 50)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x, self.rect.y = length, randrange(30, 180, 50)
        self.rect.x -= velocidade


class Ground(pg.sprite.Sprite):
    def __init__(self, pos_x):
        pg.sprite.Sprite.__init__(self)
        self.image = SpriteSheet.subsurface([192, 0], [32, 32])
        self.image = pg.transform.scale(self.image, [32 * 2, 32 * 2])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x * 64, width - 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = length
        self.rect.x -= 10


class Cactus(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = SpriteSheet.subsurface([160, 0], [32, 32])
        self.image = pg.transform.scale(self.image, [32 * 2, 32 * 2])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = length, 385
        self.mask = pg.sprite.from_surface(self.image)
        self.escolha = escolha_obstaculo

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = length
            self.rect.x -= velocidade


class DinoVoador(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprites = [SpriteSheet.subsurface([32*3,0],[32,32]),SpriteSheet.subsurface([32*4,0],[32,32])]
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pg.transform.scale(self.image,[32*3,32*3])
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = length,280
        self.mask = pg.sprite.from_surface(self.image)
        self.escolha = escolha_obstaculo

    def update(self):
        self.atual += 0.25
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]
        self.image = pg.transform.scale(self.image,[32*3,32*3])
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = length
            self.rect.x -= velocidade


todas_as_sprites = pg.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)
for a in range(21):
    if a < 4:
        cloud = Clouds()
        todas_as_sprites.add(cloud)
    ground = Ground(a)
    todas_as_sprites.add(ground)
cactus = Cactus()
todas_as_sprites.add(cactus)
dino_voador = DinoVoador()
todas_as_sprites.add(dino_voador)
grupo_colisao = pg.sprite.Group()
grupo_colisao.add(cactus,dino_voador)

while True:
    clock.tick(30)
    tela.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not colidiu:
                dino.pular()
            if event.key == K_r and colidiu:
                restart_game()

    if cactus.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0,1])
        cactus.rect.x,dino_voador.rect.x = length,length
        cactus.escolha,dino_voador.escolha = escolha_obstaculo,escolha_obstaculo

    colisoes = pg.sprite.spritecollide(dino, grupo_colisao, False, pg.sprite.collide_mask)
    todas_as_sprites.draw(tela)
    if colisoes and not colidiu: # se morreu
        death.play()
        colidiu = True
    if colidiu: # se morreu fica aparecendo as mensagem até apertar R lá nos evento
        texto_retorno1 = exibe_mensagem('GAME OVER', 60, (0, 0, 0))
        texto_retorno2 = exibe_mensagem('Pressione r para reiniciar', 25, (0, 0, 0))
        tela.blit(texto_retorno1, [230, 200])
        tela.blit(texto_retorno2, [260, 265])
    if not colidiu: # se o player tá vivo vai continuar o game normal atualizando e pontuando
        todas_as_sprites.update()
        texto_retorno = exibe_mensagem(pontos, 40, (0,0,0))
        pontos += 1
    if pontos % 100 == 0 and not colidiu: # se o player tá vivo e pontuação múltiplo de 100
        score.play()
        if velocidade <= 30:
            velocidade += 1

    tela.blit(texto_retorno,[520,30])
    pg.display.flip()