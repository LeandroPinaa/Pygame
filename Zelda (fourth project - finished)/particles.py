import pygame as pg
from support import import_folder
from random import choice

# Classe AnimationPlayer serve para importar todas as partículas assim que o jogo for iniciado, pq importar leva tempo,
# se for importar uma partícula toda vez q ela aparecer vai deixar o game lento.


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),

            # attacks
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),
            'sparkle': import_folder('graphics/particles/sparkle'),
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),
            'thunder': import_folder('graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('graphics/particles/smoke_orange'),
            'raccoon': import_folder('graphics/particles/raccoon'),
            'spirit': import_folder('graphics/particles/nova'),
            'bamboo': import_folder('graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder('graphics/particles/leaf1'),
                import_folder('graphics/particles/leaf2'),
                import_folder('graphics/particles/leaf3'),
                import_folder('graphics/particles/leaf4'),
                import_folder('graphics/particles/leaf5'),
                import_folder('graphics/particles/leaf6'),
                self.reflect_images(import_folder('graphics/particles/leaf1')),
                self.reflect_images(import_folder('graphics/particles/leaf2')),
                self.reflect_images(import_folder('graphics/particles/leaf3')),
                self.reflect_images(import_folder('graphics/particles/leaf4')),
                self.reflect_images(import_folder('graphics/particles/leaf5')),
                self.reflect_images(import_folder('graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pg.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, attack_type, pos, groups):  # when the player gets hit and when the enemy dies
        animation_frames = self.frames[attack_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.current = 0
        self.animation_frames = animation_frames
        self.image = self.animation_frames[self.current]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.current += 0.15
        if self.current >= len(self.animation_frames):
            self.kill()
        else:
            self.image = self.animation_frames[int(self.current)]

    def update(self):
        self.animate()
