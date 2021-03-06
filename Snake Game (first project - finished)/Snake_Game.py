import pygame as pg
from random import randint
from pygame.locals import *

pg.init()
pg.mixer.music.set_volume(0.5)
musica = pg.mixer.music.load('BoxCat Games - CPU Talk.mp3')
pg.mixer.music.play(-1)
collision = pg.mixer.Sound('smw_coin.wav')
length,width = 640,480
x,y,food_x,food_y = int(length/2 - 10),int(width/2 - 10),randint(0,length-20),randint(0,width-20)
fonte,score = pg.font.SysFont('arial',40,bold=True,italic=True),0
tela = pg.display.set_mode((length,width))
pg.display.set_caption('Snake Game')
clock = pg.time.Clock()
SnakeBody,comprimento_inicial,velocidade = [],10,10
x_controle,y_controle,morreu = velocidade,0,False

def SnakeGetsBigger(SnakeBody):
    for XY in SnakeBody:
        pg.draw.rect(tela,(0,255,0),[XY[0],XY[1],20,20])
def RestartGame():
    global morreu,score,SnakeBody,comprimento_inicial,velocidade,x,y,food_x,food_y
    x,y,food_x,food_y = int(length/2-10),int(width/2-10),randint(0,length-20),randint(0,width-20)
    SnakeBody,comprimento_inicial,velocidade,score = [],10,10,0
    x_controle,y_controle,morreu = velocidade,0,False

while True:
    clock.tick(40)
    tela.fill((255,255,255))
    mensagem = f'Pontos: {score}'
    texto_formatado = fonte.render(mensagem,True,(0,0,0))
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a and x_controle != velocidade: #ultima condição pra n poder pressionar A se tiver pressionado o D
                x_controle,y_controle = -velocidade,0
            if event.key == K_d and x_controle != -velocidade:
                x_controle,y_controle = velocidade,0
            if event.key == K_w and y_controle != velocidade:
                x_controle,y_controle = 0,-velocidade
            if event.key == K_s and y_controle != -velocidade:
                x_controle,y_controle = 0,velocidade
    x += x_controle
    y += y_controle

    snake = pg.draw.rect(tela, (0,255,0), [x,y,20,20])
    food = pg.draw.rect(tela, (255,0,0), [food_x,food_y,20,20])

    if snake.colliderect(food):
        food_x,food_y = randint(0,length-20),randint(0,width-20)
        score += 1
        collision.play()
        comprimento_inicial += 1

    tela.blit(texto_formatado,[400,40])

    SnakeBody.append([x, y])
    if SnakeBody.count(SnakeBody[-1]) > 1:
        fonte2 = pg.font.SysFont('arial',20,bold=True,italic=True)
        mensagem2 = 'Game Over! Pressione a tecla R para jogar novamente'
        texto_formatado2 = fonte2.render(mensagem2,True,(0,0,0))
        ret_texto = texto_formatado2.get_rect()
        morreu = True
        while morreu:
            tela.fill((255, 255, 255))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        RestartGame()
            ret_texto.center = [length//2,width//2]
            tela.blit(texto_formatado2,ret_texto)
            pg.display.update()

    if x > length:
        x = 0
    if x < 0:
        x = length
    if y > width:
        y = 0
    if y < 0:
        y = width

    if len(SnakeBody) > comprimento_inicial:
        del(SnakeBody[0])
    SnakeGetsBigger(SnakeBody)
    pg.display.update()