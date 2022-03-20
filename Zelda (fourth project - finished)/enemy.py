import pygame as pg
from settings import *
from entity import Entity
from support import *
from pygame.math import Vector2 as vec


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_in_player, trigger_death_particles, get_exp):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.animations = None
        self.status = 'idle'
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.current]

        # movement setup
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # enemy stats
        self.monster_name = monster_name
        monster_info = MONSTER_DATA[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = None
        self.damage_in_player = damage_in_player
        self.trigger_death_particles = trigger_death_particles  # when the enemy dies
        self.get_exp = get_exp

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 600

        # sound
        self.death_sound = pg.mixer.Sound('audio/death.wav')
        self.hit_sound = pg.mixer.Sound('audio/hit.wav')
        self.attack_sound = pg.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.3)
        self.hit_sound.set_volume(0.3)
        self.attack_sound.set_volume(0.2)

    def import_graphics(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        for animation in self.animations.keys():
            full_path = f'graphics/monsters/{monster_name}/{animation}'
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.current += 0.15
        if self.current >= len(animation):
            if self.status == 'attack':  # assim can_attack só vira False dps q a animação acaba
                self.can_attack = False
            self.current = 0
        self.image = animation[int(self.current)]
        self.rect = self.image.get_rect(center=self.rect.center)

        # abaixo é pra deixar o inimigo piscando quando for acertado (MTO OP)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_player_distance_direction(self, player):
        enemy_vec = vec(self.rect.center)
        player_vec = vec(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()  # com magnitude pega a distância de vdd
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()  # pega a direção
        else:
            direction = vec(0, 0)

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.current = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pg.time.get_ticks()
            self.damage_in_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = vec(0, 0)

    def cooldown(self):
        current_time = pg.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, sprite_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if sprite_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pg.time.get_ticks()
            self.hit_sound.play()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.kill()
            self.get_exp(self.exp)
            self.death_sound.play()

    def knockback(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.knockback()
        self.cooldown()
        self.move(self.speed)
        self.animate()
        self.check_death()

    def enemy_update(self, player):  # método só pra pegar o objeto player e mandar como parâmetro nos de baixo
        self.get_status(player)
        self.actions(player)
