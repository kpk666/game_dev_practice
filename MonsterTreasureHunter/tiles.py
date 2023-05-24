import pygame
from game_data import *
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))


    def update(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Goal(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface
        
class Static_objects(StaticTile):
    def __init__(self, size, x, y, ):
        super().__init__(size, x, y, pygame.image.load(path_ship).convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(topleft=(x, offset_y))

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.collision_rect = pygame.Rect(self.rect.topleft,(self.rect.width,self.rect.height))

    def animate(self):
        self.frames_index += 0.15
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = self.collision_rect.bottom
        
    def update(self, shift_x, shift_y):
        self.animate()
        self.rect.x += shift_x
        self.rect.y += shift_y
        

class Coins(AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size - 20)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value
        self.collision_rect = pygame.Rect(self.rect.topleft,(self.rect.width,self.rect.height))

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset_y, offset_x=0):
        super().__init__(size, x, y, path)
        offset_y = y - offset_y
        offset_x = x - offset_x
        self.rect = self.image.get_rect(topleft=(x, offset_y))
        self.collision_rect = pygame.Rect(self.rect.topleft,(32,self.rect.height))

class Water(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_rect = pygame.Rect(self.rect.topleft,(self.rect.width,self.rect.height))
