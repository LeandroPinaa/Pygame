import pygame as pg
from pygame.math import Vector2 as vec
from os import walk
from support import *
from settings import *
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_weapon, destroy_weapon, create_magic, restarted_or_not=False, restarted_stats=None):
        super().__init__(groups)
        self.image = pg.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, -26)  # y era -26
        # animations/sprites
        self.animations = None  # it's going to be a dict, way more organized
        self.import_player_animations()
        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.status = 'down_idle'
        self.obstacle_sprites = obstacle_sprites
        # weapon
        self.create_weapon = create_weapon
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(MAGIC_DATA.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        # player stats
        if not restarted_or_not:
            self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        else:
            self.stats = restarted_stats
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 0
        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 500
        # music and sound
        self.weapon_attack_sound = pg.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.05)

    def import_player_animations(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = 'graphics/player/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.current += 0.15
        if self.current >= len(animation):
            self.current = 0
        self.image = animation[int(self.current)]
        self.rect = self.image.get_rect(center=self.rect.center)

        # abaixo é pra deixar o player piscando quando for acertado (MTO OP)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def input(self):
        if not self.attacking:
            # movement input
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.direction[0] = -1
                self.status = 'left'
            elif keys[pg.K_RIGHT]:
                self.direction[0] = 1
                self.status = 'right'
            else:
                self.direction[0] = 0
            if keys[pg.K_UP]:
                self.direction[1] = -1
                self.status = 'up'
            elif keys[pg.K_DOWN]:
                self.direction[1] = 1
                self.status = 'down'
            else:
                self.direction[1] = 0

            # attack input
            if keys[pg.K_SPACE]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                self.create_weapon()
                self.weapon_attack_sound.play()
            # magic input
            if keys[pg.K_c]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                style = list(MAGIC_DATA.keys())[self.magic_index]
                strength = list(MAGIC_DATA.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(MAGIC_DATA.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
            # changing weapon input
            if keys[pg.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pg.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(list(WEAPON_DATA.keys())):
                    self.weapon_index = 0
                self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
            # changing magic input
            if keys[pg.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pg.time.get_ticks()
                self.magic_index += 1
                if self.magic_index >= len(list(MAGIC_DATA.keys())):
                    self.magic_index = 0
                self.magic = list(MAGIC_DATA.keys())[self.magic_index]

    def get_status(self):
        if self.direction == vec(0, 0) and 'idle' not in self.status and 'attack' not in self.status:
            self.status += '_idle'
        if self.attacking:
            self.direction = vec(0, 0)
            if 'attack' not in self.status:
                if 'idle' not in self.status:
                    self.status += '_attack'
                else:
                    self.status = self.status.replace('_idle', '_attack')
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '_idle')

    def cooldown(self):  # timer between attacks
        current_time = pg.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + WEAPON_DATA[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_weapon()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = WEAPON_DATA[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        basic_damage = self.stats['magic']
        spell_damage = MAGIC_DATA[self.magic]['strength']
        return basic_damage + spell_damage

    def get_basic_value(self, index):
        attribute_values = list(self.stats.values())[index]
        return attribute_values

    def get_cost_value(self, index):
        cost_values = list(self.upgrade_cost.values())[index]
        return cost_values

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.004 * self.stats['magic']

    def update(self):
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
