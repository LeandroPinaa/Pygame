import pygame as pg
from settings import *
from tile import Tile
from player import Player
from pygame.math import Vector2 as vec
from support import *
from random import choice, randint
from debug import debug
from weapon import Weapon
from UI import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


# a classe Level conterá os grupos de sprites q serão desenhados na tela e várias outras coisas, como player, tile


class Level:
    def __init__(self, restarted_or_not=False, restarted_stats=None):
        # get the display surface aka self.screen anywhere on the code
        self.display_surface = pg.display.get_surface()
        self.main_sound = pg.mixer.Sound('audio/main.ogg')
        self.main_sound.set_volume(0.3)
        self.main_sound.play(-1)

        # sprites group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()
        self.attack_sprites = pg.sprite.Group()  # aqui sprites das armas
        self.attackable_sprites = pg.sprite.Group()  # aqui sprites dos monstros, q serão atacados com as armas

        # restarted_or_not setup (in case the player already cleared map)
        self.restarted_or_not = restarted_or_not
        self.restarted_stats = restarted_stats

        # sprites setup
        self.player = None
        self.current_weapon = None
        self.create_map()

        # user interface
        self.ui = UI()
        self.game_paused = False
        self.upgrade = Upgrade(self.player)

        # particles imported
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # after killing enemies setup
        self.waiting, self.can_click = None, None
        self.time_to_display_others, self.short_timer = None, None
        self.big_font = pg.font.Font(UI_FONT, 30)
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        self.small_font = pg.font.Font(UI_FONT, 13)
        self.main_rect = pg.Rect(WIDTH // 2, HEIGHT, 600, 300)
        self.main_rect.center = (WIDTH // 2, HEIGHT+500)
        self.first_text_surf = self.big_font.render('LEVEL COMPLETED!', True, TEXT_COLOR)
        self.first_text_rect = self.first_text_surf.get_rect(center=(WIDTH//2, HEIGHT + 420))
        self.second_text_surf = self.font.render('CONGRATS :)', True, TEXT_COLOR)
        self.second_text_rect = self.second_text_surf.get_rect(center=(WIDTH//2, HEIGHT//2-45))
        self.third_text_surf = self.font.render('DO YOU WANT TO RESTART THE MAP?', True, TEXT_COLOR)
        self.third_text_rect = self.third_text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.yes_surf = self.font.render('(Y)YES', True, GREEN)
        self.yes_rect = self.yes_surf.get_rect(center=(WIDTH//2-90, HEIGHT//2+30))
        self.no_surf = self.font.render('(N)NO', True, RED)
        self.no_rect = self.no_surf.get_rect(center=(WIDTH//2+70, HEIGHT//2+30))
        self.fourth_text_surf = self.small_font.render('OBS: YOU WON\'T LOSE YOUR CURRENT STATS PROGRESS', False, TEXT_COLOR)
        self.fourth_text_rect = self.fourth_text_surf.get_rect(center=(WIDTH//2, HEIGHT//2+130))
        self.zelda_congrats_sound = pg.mixer.Sound('audio/zelda_congrats.mp3')
        self.zelda_congrats_sound.set_volume(0.5)

        # game over setup
        self.game_over_sound = pg.mixer.Sound('audio/game_over.mp3')
        self.game_over_sound.set_volume(0.5)
        self.huge_font = pg.font.Font(UI_FONT, 50)
        self.game_over_surf = self.huge_font.render('GAME OVER', False, TEXT_COLOR)
        self.game_over_rect = self.game_over_surf.get_rect(center=(WIDTH//2, HEIGHT + 420))
        self.fifth_text_surf = self.small_font.render('better luck next time :(', True, TEXT_COLOR)
        self.fifth_text_rect = self.fifth_text_surf.get_rect(center=(WIDTH//2, HEIGHT//2-45))

    def create_map(self):
        layouts = {  # dicionário com o mapa. boundary são os blocos limites, grass grama e object os objetos
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }
        for style, layout in layouts.items():  # style sendo a chave e layout sendo os valores
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                                     self.create_weapon, self.destroy_weapon, self.create_magic,
                                                     self.restarted_or_not, self.restarted_stats)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_in_player, self.trigger_death_particles,
                                      self.get_exp)

    def create_weapon(self):
        self.current_weapon = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_weapon(self):
        if self.current_weapon:
            self.current_weapon.kill()
        self.current_weapon = None

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self):  # when the player hits with weapon/magic then enemy or opposite
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision = pg.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision:
                    for target_sprite in collision:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos, [self.visible_sprites])
                            target_sprite.kill()
                        else:  # enemy
                            # caso colida eu chamo get_damage pra calcular o dano, mas antes preciso saber oq o player
                            # tá fazendo e com q tipo de arma ele atacou, weapon ou magic
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_in_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health = int(self.player.health - amount)
            if self.player.health < 0:
                self.player.health = 0
            self.player.vulnerable = False
            self.player.hit_time = pg.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):  # when the enemy dies
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def get_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def waiting_decision(self, clock):
        self.waiting, self.can_click = True, False
        while self.waiting:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            pg.draw.rect(self.display_surface, UI_BG_COLOR, self.main_rect)
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR, self.main_rect, 3)
            self.display_surface.blit(self.first_text_surf, self.first_text_rect)
            if self.main_rect.center != (WIDTH//2, HEIGHT//2):
                self.main_rect[1] -= 10
                self.first_text_rect[1] -= 10
            else:  # if the rect is in the pos I want, then the player can click quit yes or no
                self.time_to_display_others = pg.time.get_ticks()
                if self.time_to_display_others > 4000:
                    self.display_surface.blit(self.second_text_surf, self.second_text_rect)
                if self.time_to_display_others > 6000:
                    self.can_click = True
                    self.display_surface.blit(self.third_text_surf, self.third_text_rect)
                    self.display_surface.blit(self.yes_surf, self.yes_rect)
                    self.display_surface.blit(self.no_surf, self.no_rect)
                    self.display_surface.blit(self.fourth_text_surf, self.fourth_text_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y and self.can_click:
                        self.waiting = False
                        self.restart_game()
                    elif event.key == pg.K_n and self.can_click:
                        pg.quit()
                        exit()
            pg.display.flip()
            clock.tick(FPS)

    def waiting_death_decision(self, clock):
        self.waiting, self.can_click = True, False
        while self.waiting:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            pg.draw.rect(self.display_surface, UI_BG_COLOR, self.main_rect)
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR, self.main_rect, 3)
            self.display_surface.blit(self.game_over_surf, self.game_over_rect)
            if self.main_rect.center != (WIDTH//2, HEIGHT//2):
                self.main_rect[1] -= 10
                self.game_over_rect[1] -= 10
            else:
                self.time_to_display_others = pg.time.get_ticks()
                if self.time_to_display_others > 4000:
                    self.display_surface.blit(self.fifth_text_surf, self.fifth_text_rect)
                if self.time_to_display_others > 6000:
                    self.can_click = True
                    self.display_surface.blit(self.third_text_surf, self.third_text_rect)
                    self.display_surface.blit(self.yes_surf, self.yes_rect)
                    self.display_surface.blit(self.no_surf, self.no_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y and self.can_click:
                        self.waiting = False
                        self.restart_game()
                    elif event.key == pg.K_n and self.can_click:
                        pg.quit()
                        exit()
            pg.display.flip()
            clock.tick(FPS)

    def restart_game(self):
        restarted_or_not = True
        self.zelda_congrats_sound.stop()
        self.game_over_sound.stop()
        self.__init__(restarted_or_not, self.player.stats)

    def run(self, clock):
        # I want to display those two below even when the game is paused as well
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.player.health <= 0:
            self.main_sound.stop()
            self.game_over_sound.play()
            self.short_timer = pg.time.get_ticks()
            if self.short_timer > 1000:
                self.waiting_death_decision(clock)
        if self.visible_sprites.enemy_update(self.player):  # if returns True it means there's no more enemies
            self.main_sound.stop()
            self.zelda_congrats_sound.play(-1)
            self.short_timer = pg.time.get_ticks()
            if self.short_timer > 1000:  # wait just a little to show the level completed screen
                self.waiting_decision(clock)

        if self.game_paused:  # displays upgrade menu
            self.upgrade.display()
        else:  # runs the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


# essa classe tem a intenção de mudar o atributo self.visible_sprites. Normalmente um grupo de sprites serve para
# desenhar elas na tela ou dar update, porém, vou adicionar um método a mais, o custom draw, que irá deixar mais
# otimizado o draw como também ira influenciar na câmera. Basicamente eu crio um self.offset (eu explico nos
# comentários) e + 2 atributos q possuem o valor da metade da tela. Com isso, no custom_draw, eu influencio o meu
# self.offset de acordo com as coordenadas do player, toda a linha do custom_draw é importante pra isso funcionar.
class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = vec(0, 0)  # determina a posição inicial em que desenha as sprites, se fizer 100,200 vai entender

        # creating the floor
        self.floor_surf = pg.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # changing offset based on the player's position
        self.offset[0] = player.rect.centerx - self.half_width
        self.offset[1] = player.rect.centery - self.half_height

        # drawing the floor
        offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                         and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

        if not enemy_sprites:
            return True
        return False
