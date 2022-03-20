import pygame as pg
from settings import *

# USER INTERFACE: tela do usuário com vida, energia, exp, todas as estatistícas gerais


class UI:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        self.health_bar_rect = pg.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        # draw bar
        pg.draw.rect(self.display_surface, color, current_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)  # border of bar

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)  # nesse caso AA false pq é arquivo pixelado
        text_rect = text_surf.get_rect(bottomright=(WIDTH-20, HEIGHT-20))
        pg.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def show_numbers(self, health, max_health, energy, max_energy):
        font = pg.font.Font(UI_FONT, 15)
        health_text_surf = font.render(f'{int(health)}/{int(max_health)}', True, TEXT_COLOR)
        health_text_rect = health_text_surf.get_rect(topleft=(65, 10))
        self.display_surface.blit(health_text_surf, health_text_rect)
        energy_text_surf = font.render(f'{int(energy)}/{int(max_energy)}', True, TEXT_COLOR)
        energy_text_rect = energy_text_surf.get_rect(topleft=(50, 34))
        self.display_surface.blit(energy_text_surf, energy_text_rect)

    def selection_box(self, x, y, can_switch):
        bg_rect = pg.Rect(x, y, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if can_switch:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        else:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon, weapon_rect):  # box that shows your current weapon
        full_path = f'graphics/weapons/{weapon}/full.png'
        image = pg.image.load(full_path).convert_alpha()
        image_rect = image.get_rect(center=weapon_rect.center)
        self.display_surface.blit(image, image_rect)

    def magic_overlay(self, magic_index, magic_rect):  # box that shows your current magic
        g = 'graphic'
        full_path = list(MAGIC_DATA.values())[magic_index][g]
        image = pg.image.load(full_path).convert_alpha()
        image_rect = image.get_rect(center=magic_rect.center)
        self.display_surface.blit(image, image_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)
        weapon_rect = self.selection_box(10, 630, player.can_switch_weapon)  # weapon
        magic_rect = self.selection_box(80, 635, player.can_switch_magic)  # magic
        self.weapon_overlay(player.weapon, weapon_rect)
        self.magic_overlay(player.magic_index, magic_rect)
        self.show_numbers(player.health, player.stats['health'], player.energy, player.stats['energy'])
