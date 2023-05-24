import pygame
from settings import *
from support import import_folder
from math import sin
from game_data import sounds_path

FPS = 60
dust_path = f'player1\\pink_monster\\dust_particles\\'
land_path = f'player1\\pink_monster\\'
player_animation_files_path = f'player1\\pink_monster\\'

class Player2(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()      
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animations = {'idle': self.load_sprites_shift(player_animation_files_path, 'Pink_Monster_Idle_4.png', tile_size),
                           'run': self.load_sprites_shift(player_animation_files_path, 'Pink_Monster_Run_6.png', tile_size),
                           'jump':self.load_sprites_shift(player_animation_files_path, 'Pink_Monster_Jump_8.png', tile_size),
                           'fall':self.load_sprites_shift(player_animation_files_path, 'Pink_Monster_Fall_1.png', tile_size),
                           'hurt':self.load_sprites_shift(player_animation_files_path, 'Pink_Monster_Hurt_4.png', tile_size)
                           }      
        self.image = self.animations['idle'][self.frame_index]
        self.mask = None
        self.rect = self.image.get_rect(topleft = pos)

        # Sounds
        self.player_hurt = pygame.mixer.Sound(sounds_path + 'player_hurt.mp3')
        self.jump_sound = pygame.mixer.Sound(sounds_path + 'player_jump.wav')
        self.jump_sound.set_volume(0.7)
        # dust setup
        self.import_dust_particles()
        self.dust_status = None
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles  

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))


        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.hurt = False
        self.jump_status = False
        self.jump_time = 0
        self.jump_duration = 200

        # health manegement
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 700
        self.hurt_time = 0
        
    def load_sprites_shift(self, path, name, tile_size):
        surface = pygame.image.load(path + name).convert_alpha()
        surface = pygame.transform.scale2x(surface)
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

    def get_damage(self):
        if not self.invincible:
            self.player_hurt.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def heal(self, value):
        self.change_health(value)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0
    
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def import_land_assets(self):
        character_path = land_path
        self.animators = {'land':[]}
        for animation in self.animators.keys():
            full_path = character_path + animation
            self.animators[animation] = import_folder(full_path)


    def import_dust_particles(self):
        character_path = dust_path
        self.animators = {'run':[]}
        for animation in self.animators.keys():
            full_path = character_path + animation
            self.animators[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)] 
        self.mask = pygame.mask.from_surface(image)       
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.bottomright = self.collision_rect.bottomright
            
        # if self.invincible:
        #     alpha = self.wave_value()
        #     self.image.set_alpha(alpha)
        # else:
        #     self.image.set_alpha(255)
       
        
    def dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.animators['run']):
                self.dust_frame_index = 0
            dust_particle = self.animators['run'][int(self.dust_frame_index)]
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:                
                dust_particle = pygame.transform.flip(dust_particle, True, False)
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True            
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False            
        else:
            self.direction.x = 0
        if keys[pygame.K_UP] and self.on_ground:            
                self.jump()
                self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.invincible:
            self.status = 'hurt'
        elif self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0.9:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y
    
    def jump(self):
        if not self.jump_status:
            self.jump_status == True
            self.jump_time = pygame.time.get_ticks()
            self.jump_sound.play()
            self.direction.y = self.jump_speed
            if self.jump_time >= self.jump_duration:
                self.jump_status == False

    def update(self):
        self.get_input() 
        self.get_status() 
        self.animate() 
        self.dust_animation()   
        self.invincibility_timer() 
        self.wave_value()
        