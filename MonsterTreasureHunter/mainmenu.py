import pygame
from settings import *



class MainMenu(pygame.sprite.Sprite):
    def __init__(self, surface, create_overworld):
        self.display_surface = surface
        self.background = pygame.image.load(f'Backgrounds\\game_background_2.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (screen_widht, screen_height))
        self.background_x = 0
        self.background_y = 0

        # text
        self.font_name = pygame.font.Font(f'font\\ThaleahFat.ttf', 100)
        self.game_title1 = self.font_name.render('MONSTER TREASURE', True, (250, 107, 12))
        self.game_title2 = self.font_name.render('HUNTER', True, (250, 107, 12))
        self.title1_rect = self.game_title1.get_rect(topleft = (170, 20))
        self.title2_rect = self.game_title2.get_rect(topleft = (400, 130))

        # icons
        self.start_icon = pygame.image.load(f'menu\\Btns_Green_start.png').convert_alpha()
        self.start_icon = pygame.transform.scale(self.start_icon, (240, 100))
        self.start_icon_rect = self.start_icon.get_rect(topleft=(600, 300))
        self.exit_icon = pygame.image.load(f'menu\\Btns_Green_exit.png').convert_alpha()
        self.exit_icon = pygame.transform.scale(self.exit_icon, (240, 100))
        self.exit_icon_rect = self.exit_icon.get_rect(topleft=(600, 450))
        self.create_overworld = create_overworld
        self.mouse = pygame.mouse.get_pos()
        
    def background_scroll(self):
        self.background_x -= 0.5    
        if self.background_x <= 0 - screen_widht:
            self.background_x = 0
    
    def icon_activate(self):
        action1 = False
        action2 = False
    
		#get mouse position
        pos = pygame.mouse.get_pos()
		#check mouseover and clicked conditions
        if self.start_icon_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action1 = True
                self.clicked = True
                self.create_overworld(0, 0)
                return action1
        elif self.exit_icon_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action2 = True
                self.clicked = True                
                pygame.quit()
                return action2
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        self.display_surface.blit(self.background, (self.background_x, self.background_y))
        self.display_surface.blit(self.background, (self.background_x + screen_widht, self.background_y))
        self.display_surface.blit(self.start_icon, self.start_icon_rect)
        self.display_surface.blit(self.exit_icon, self.exit_icon_rect)
        self.display_surface.blit(self.exit_icon, self.exit_icon_rect)
        self.display_surface.blit(self.game_title1, self.title1_rect)
        self.display_surface.blit(self.game_title2, self.title2_rect)

        

    def run(self):
        self.icon_activate()                     
        self.background_scroll()

class GameOver:
    def __init__(self, surface, create_overworld):
        self.display_surface = surface
        self.background = pygame.image.load(f'Backgrounds\\game_background_4.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (screen_widht, screen_height))
        self.background_x = 0
        self.background_y = 0
        self.create_overworld = create_overworld
        # text
        self.font_gv= pygame.font.Font(f'font\\ThaleahFat.ttf', 70)
        self.font_rs = pygame.font.Font(f'font\\ThaleahFat.ttf', 40)
        self.gameover = self.font_gv.render('GAME OVER!', True, (92, 20, 3)) 
        self.gameover_rect = self.gameover.get_rect(topleft=(300, 200))
        self.restart_game = self.font_rs.render('Restart game', True, (135, 30, 5))
        self.restart_game_rect = self.restart_game.get_rect(topleft=(400, 400))
        self.quit_game = self.font_rs.render('Quit game', True, (135, 30, 5))
        self.quit_game_rect = self.quit_game.get_rect(topleft=(400, 500))

    def background_scroll(self):
        self.background_x -= 0.5    
        if self.background_x <= 0 - screen_widht:
            self.background_x = 0

    def icon_activate(self):
        action1 = False
        action2 = False
    
		#get mouse position
        pos = pygame.mouse.get_pos()
		#check mouseover and clicked conditions
        if self.restart_game_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action1 = True
                self.clicked = True
                self.create_overworld(0, 0)
                return action1
        elif self.quit_game_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action2 = True
                self.clicked = True                
                pygame.quit()
                return action2
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.display_surface.blit(self.background, (self.background_x, self.background_y))
        self.display_surface.blit(self.background, (self.background_x + screen_widht, self.background_y))
        self.display_surface.blit(self.gameover, self.gameover_rect)
        self.display_surface.blit(self.restart_game, self.restart_game_rect)
        self.display_surface.blit(self.quit_game, self.quit_game_rect)
    def run(self):
        self.icon_activate()                     
        self.background_scroll()

class WinPage:
    def __init__(self, surface):
        self.display_surface = surface
        self.background = pygame.image.load(f'Backgrounds\\end.jpg').convert_alpha()
        self.background = pygame.transform.scale(self.background, (screen_widht, screen_height))
        self.background_x = 0
        self.background_y = 0
        # text
        self.font_ed = pygame.font.Font(f'font\\ThaleahFat.ttf', 70)
        self.end_game_str1 = self.font_ed.render('CONGRATULATION!!!', True, (255, 162, 0))
        self.end_game_str2 = self.font_ed.render('YOU`VE MANAGED TO COLLECT', True, (255, 162, 0))
        self.end_game_str3 = self.font_ed.render('ALL COINS AND SURVIVED', True, (255, 162, 0))
        self.end_game_thx = self.font_ed.render('THANK YOU FOR PLAYING!', True, (255, 162, 0))
        self.end_game_str1_rect = self.end_game_str1.get_rect(topleft = (380, 100))
        self.end_game_str2_rect = self.end_game_str2.get_rect(topleft = (380, 200))
        self.end_game_str3_rect = self.end_game_str3.get_rect(topleft = (380, 300))
        self.end_game_thx_rect = self.end_game_thx.get_rect(topleft = (380, 400))

        self.display_surface.blit(self.background, (self.background_x, self.background_y))
        self.display_surface.blit(self.end_game_str1, self.end_game_str1_rect)
        self.display_surface.blit(self.end_game_str2, self.end_game_str2_rect)
        self.display_surface.blit(self.end_game_str3, self.end_game_str3_rect)
        self.display_surface.blit(self.end_game_thx, self.end_game_thx_rect)
    
    def background_scroll(self):
        self.background_x -= 0.1    
        if self.background_x <= 0 - 2:
            self.background_x += 0.1
        elif self.background_x >= screen_widht + 2:
            self.background_x -= 0.1
    def icon_activate(self):
        action = False

    
		#get mouse position
        pos = pygame.mouse.get_pos()
		#check mouseover and clicked conditions
        if self.end_game_thx_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True                
                pygame.quit()
                return action
    
    def run(self):
        self.icon_activate()
        self.background_scroll()