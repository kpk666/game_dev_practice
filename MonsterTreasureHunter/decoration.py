import pygame
from settings import vertical_tile_number, tile_size, screen_widht
from tiles import AnimatedTile, StaticTile
from game_data import path_water
from support import import_folder
from random import choice, randint


class Sky:
    def __init__(self, horizont, style = 'level'):
        self.bottom = pygame.image.load(f'sky\\sky_bottom.png').convert()
        self.top = pygame.image.load(f'sky\\sky_top.png').convert()
        self.middle = pygame.image.load(f'sky\\sky_middle.png').convert()
        self.horizont = horizont
        # scretch
        self.top = pygame.transform.scale(self.top, (screen_widht, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_widht, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_widht, tile_size))
        self.style = style
        if self.style == 'overworld':
            palm_surface = import_folder(f'overworld\\palms')
            self.palms = []
            for surface in [choice(palm_surface) for image in range(10)]:
                x = randint(5, screen_widht)
                y = (self.horizont * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom = (x, y))
                self.palms.append((surface, rect))
            clouds_surface = import_folder(f'overworld\\clouds')
            self.clouds = []
            for surface in [choice(clouds_surface) for image in range(10)]:
                x = randint(5, screen_widht)
                y = randint(0, (self.horizont * tile_size) - 100)
                rect = surface.get_rect(midbottom = (x, y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizont:
                surface.blit(self.top, (0, y))
            elif row == self.horizont:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))
        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])

class Water:
    def __init__(self, top, level_width):
        water_start = -screen_widht
        water_tile_width = 64
        tile_x_amount = int((level_width + screen_widht) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()
        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(64, x, y, path_water)
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)

class Clouds:
    def __init__(self, horizont, level_width, clouds_number):
        cloud_surf_list = import_folder(f"clouds")
        min_x = -screen_widht
        max_x = level_width + screen_widht
        min_y = 0
        max_y = horizont
        self.clouds_sprites = pygame.sprite.Group()
        for cloud in range(clouds_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.clouds_sprites.add(sprite)

    def draw(self, surface, shift_x, shift_y):
        self.clouds_sprites.update(shift_x, shift_y)
        self.clouds_sprites.draw(surface)