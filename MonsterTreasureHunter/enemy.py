import pygame
from tiles import AnimatedTile
from game_data import path_enemies_run
from random import randint
class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, path_enemies_run)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)
        self.collision_rect = pygame.Rect(self.rect.topleft,(self.rect.width,self.rect.height))

    def move(self):
        self.rect.x += self.speed 

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y
        self.animate()
        self.move()
        self.reverse_image()