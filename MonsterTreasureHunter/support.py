from csv import reader
import pygame
from settings import tile_size
from os import listdir, walk
from os.path import isfile, join


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphics_one_file(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)
    return cut_tiles

def import_cut_graphics(path):    
    images = [f for f in listdir(path) if isfile(join(path, f))]
    cut_tiles = []    
    for image in images:
        sprite = pygame.image.load(join(path, image)).convert_alpha()
        sprite_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
        sprite_surface.blit(sprite, (0, 0), pygame.Rect(0, 0, tile_size, tile_size))
        cut_tiles.append(pygame.transform.scale(sprite_surface, (tile_size, tile_size)))
    return cut_tiles

def import_cut_graphics_objects(path):    
    images = [f for f in listdir(path) if isfile(join(path, f))]
    cut_tiles = []    
    for image in images:
        sprite = pygame.image.load(join(path, image)).convert_alpha()
        sprite_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
        sprite_surface.blit(sprite, (0, 0), pygame.Rect(0, 0, tile_size, tile_size))
        cut_tiles.append(sprite_surface)
    return cut_tiles

def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = join(path, image) 
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list