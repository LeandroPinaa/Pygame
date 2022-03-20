import pygame as pg
from settings import *
from pygame.math import Vector2 as vec


class Upgrade:
    def __init__(self, player):
        self.display_surface = pg.display.get_surface()
        self.player = player
        self.attribute_number = len(self.player.stats)
        self.attribute_names = list(self.player.stats.keys())
        self.attribute_max_values = list(self.player.max_stats.values())
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        # each upgrade bar dimensions
        self.width = self.display_surface.get_width() // 6
        self.height = self.display_surface.get_height() * 0.8
        self.upgrade_bar_list = None
        self.create_upgrade_bar()

    def input(self):
        keys = pg.key.get_pressed()
        if self.can_move:
            if keys[pg.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.selection_time = pg.time.get_ticks()
                self.can_move = False

            elif keys[pg.K_LEFT] and self.selection_index > 0:
                self.selection_index -= 1
                self.selection_time = pg.time.get_ticks()
                self.can_move = False

            if keys[pg.K_SPACE]:
                self.selection_time = pg.time.get_ticks()
                self.can_move = False
                self.upgrade_bar_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        current_time = pg.time.get_ticks()
        if not self.can_move:
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_upgrade_bar(self):
        self.upgrade_bar_list = []

        for upgrade_bar in range(self.attribute_number):
            # getting the coordinates of the topleft side of each upgrade bar
            full_width = self.display_surface.get_width()
            increment = full_width // self.attribute_number
            x = (upgrade_bar * increment) + (increment - self.width) // 2
            y = self.display_surface.get_height() * 0.1

            item = UpgradeBar(x, y, self.width, self.height, upgrade_bar, self.font)
            self.upgrade_bar_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, upgrade_bar in enumerate(self.upgrade_bar_list):
            # get attributes for each upgrade bar
            name = self.attribute_names[index]
            value = self.player.get_basic_value(index)
            max_value = self.attribute_max_values[index]
            cost = self.player.get_cost_value(index)

            upgrade_bar.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class UpgradeBar:
    def __init__(self, x, y, w, h, index, font):
        self.rect = pg.Rect(x, y, w, h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected, value, max_value):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + vec(0, 20))
        surface.blit(title_surf, title_rect)

        # cost
        if value != max_value:
            cost_surf = self.font.render(f'{int(cost)}', False, color)
            cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - vec(0, 20))
            surface.blit(cost_surf, cost_rect)
        else:
            max_surf = self.font.render('MAXED', False, color)
            max_rect = max_surf.get_rect(midbottom=self.rect.midbottom - vec(0, 20))
            surface.blit(max_surf, max_rect)

    def display_bar(self, surface, value, max_value, selected):
        # drawing setup
        top = self.rect.midtop + vec(0, 60)
        bottom = self.rect.midbottom - vec(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pg.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # drawing elements
        pg.draw.line(surface, color, top, bottom, 5)
        pg.draw.rect(surface, color, value_rect)

    def trigger(self, player):  # to upgrade the stats when pressed space
        upgrade_attribute = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[upgrade_attribute]:
            if player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
                player.exp -= player.upgrade_cost[upgrade_attribute]  # we lower the player exp
                player.stats[upgrade_attribute] = player.stats[upgrade_attribute] * 1.2  # we increase the stat
                player.upgrade_cost[upgrade_attribute] *= 1.4  # we increase the basic cost from the specific stats
            if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:  # caso chegue no max
                player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_index, name, value, max_value, cost):
        if self.index == selection_index:  # highlight the upgrade bar we are in
            pg.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)  # UPGRADE_BG_COLOR_SELECTED = branco
            pg.draw.rect(surface, UI_BORDER_COLOR_ACTIVE, self.rect, 4)
        else:
            pg.draw.rect(surface, UI_BG_COLOR, self.rect)
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, cost, self.index == selection_index, value, max_value)
        self.display_bar(surface, value, max_value, self.index == selection_index)
