from csv import reader
from os import walk
import pygame as pg


#  para arquivos csv e outros
def import_csv_layout(path):
    terrain_map = list()
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


# para importar pastas e organizar
def import_folder(path):
    surface_list = list()
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
