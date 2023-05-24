import pygame, sys
from os.path import join
from overworld import *
from settings import *
from level import Level
from ui import *
from game_data import music_path
from mainmenu import MainMenu, GameOver, WinPage

class Game:
    def __init__(self):
        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        self.mainmenu = MainMenu(screen, self.create_overworld)
        self.status = 'mainmenu'
        self.end_game = 0

        # Music
        self.mainmenu_music = pygame.mixer.Sound(music_path + 'mainmenu.mp3')
        self.level_1_bg_music = pygame.mixer.Sound(music_path + 'level_1.mp3')
        self.level_2_bg_music = pygame.mixer.Sound(music_path + 'Level_2.mp3')
        self.level_3_bg_music = pygame.mixer.Sound(music_path + 'Level_3.mp3')
        self.level_4_bg_music = pygame.mixer.Sound(music_path + 'Level_4.mp3')
        self.overworld_bg_music = pygame.mixer.Sound(music_path + 'overworld.mp3')
        self.winpage_music = pygame.mixer.Sound(music_path + 'winpage.mp3')
        self.gameover_bg_music = pygame.mixer.Sound(music_path + 'Gameover.mp3')
        self.mainmenu_music.set_volume(0.7)
        self.level_1_bg_music.set_volume(0.7)
        self.level_2_bg_music.set_volume(0.7)
        self.level_3_bg_music.set_volume(0.7)
        self.level_4_bg_music.set_volume(0.7)
        self.overworld_bg_music.set_volume(0.7)
        self.mainmenu_music.play(loops = -1)

        # user interface
        self.ui = UI(screen)


    # def main_title(self):
    #     self.status = 'Main menu'
    #     self.mainmenu = MainMenu(screen, self.create_overworld)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health, self.check_game_over, self.finish_game)
        self.status = 'level'
        self.overworld_bg_music.stop()
        if current_level == 0:
            self.level_1_bg_music.play(-1)
        elif current_level == 1:
            self.level_2_bg_music.play(-1)
        elif current_level == 2:
            self.level_3_bg_music.play(-1)
        elif current_level == 3:
            self.level_4_bg_music.play(-1)

    def create_overworld(self, current_level, new_max_level):
        self.mainmenu_music.stop()
        self.level_1_bg_music.stop()
        self.level_2_bg_music.stop()
        self.level_3_bg_music.stop()
        self.level_4_bg_music.stop()
        self.gameover_bg_music.stop()
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)
        self.coins = 0

    def change_coins(self, amount):
        self.coins += amount

    def finish_game(self):
        self.end_game += 1

    def change_health(self, amount):
        self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = 100

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            self.max_level = 0 
            self.level_1_bg_music.stop()
            self.level_2_bg_music.stop()
            self.level_3_bg_music.stop()
            self.level_4_bg_music.stop()
            self.overworld_bg_music.stop()
            self.game_over = GameOver(screen, self.create_overworld)
            self.status = 'gameover'            
            self.gameover_bg_music.play(loops = -1)

    def check_end_game(self):
            if self.end_game >= 1:
                self.level_1_bg_music.stop()
                self.level_2_bg_music.stop()
                self.level_3_bg_music.stop()
                self.level_4_bg_music.stop()
                self.winpage_music.play(loops = -1)
                self.end_game = WinPage(screen)
                self.status = 'win_page'

    def run(self):
        if self.status == 'mainmenu':
            self.mainmenu.run()
        elif self.status == 'gameover':
            self.game_over.run()
        elif self.status == 'win_page':
            self.end_game.run()  
        elif self.status == 'overworld':
            self.overworld.run()       
        elif self.status == 'level':
            self.level.draw()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()
            self.check_end_game()

WIDHT, HEIGHT = 1024, 768
FPS = 60
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((screen_widht, screen_height))
pygame.display.set_caption("MONSTER TREASURE HUNTER")
icon = pygame.image.load(f'icon\\icon.png')
pygame.display.set_icon(icon) 
mouse = pygame.mouse.get_pos()
# level_1 = Level(level_0, screen)
game = Game()

def get_background(name):
    bg = pygame.image.load(f'Backgrounds' + name)
    bg = pygame.transform.scale(bg, (WIDHT, HEIGHT))
    return bg
    

def main():
    game_run = True
    clock = pygame.time.Clock()
    while game_run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:            
                game_run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_run = False
                    break

        # screen.fill('grey')
        game.run()
        pygame.display.update()
    pygame.quit()
    quit()
if __name__ == "__main__":
    main()