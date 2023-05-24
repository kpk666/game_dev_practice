import pygame
from game_data import path_health_bar, path_coin_bar, path_font


class UI:
    def __init__(self, surface):
        super().__init__()
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load(path_health_bar).convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin_bar = pygame.image.load(path_coin_bar).convert_alpha()
        self.coin_rect = self.coin_bar.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font(path_font, 25)
        # self.font_coin_surface = self.font.render('3', True, (100, 100, 200))

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect((self.health_bar_topleft),(current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface,'#dc4949', health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin_bar, self.coin_rect)
        coins_amount_surf = self.font.render(str(amount), True, '#33323d')
        coins_amount_rect = coins_amount_surf.get_rect(midleft=(self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coins_amount_surf, coins_amount_rect)