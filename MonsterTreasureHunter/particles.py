import pygame
from support import import_folder
from Player import dust_path
path_expl = f'enemy\\'

class ParticalEffects(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'jump':
            self.frames = import_folder(dust_path + 'jump\\')
        if type == 'land':
            self.frames = import_folder(dust_path + 'land\\')
        if type == 'explosion':
            self.frames = import_folder(path_expl + 'explosion\\')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    def update(self, x_shift, y_shift):
        self.animate()
        self.rect.x += x_shift
        self.rect.y += y_shift