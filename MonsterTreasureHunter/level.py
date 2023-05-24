import pygame
from support import *
from settings import *
from tiles import Tile, StaticTile, Coins, Palm, AnimatedTile
from game_data import *
from enemy import Enemy
from decoration import *
from Player import Player2
from particles import ParticalEffects

class Level:

    def __init__(self, current_level,surface, create_overworld, change_coins, change_health, check_game_over, finish_game): # extract level_data
        # GENERAL SETUP
        self.display_surface = surface
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.current_x = 0
        self.win_points = 0
        self.check_game_over = check_game_over
        self.finish_game = finish_game
        
        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.max_new_level = level_data['unlock'] 

        # win conditions
        self.win_conditions = 'Locked'
        if self.current_level == 0:
            if self.win_points >= 17:
                self.win_conditions = 'opened'
        if self.current_level == 1:
            if self.win_points >= 27:
                self.win_conditions = 'opened'
        if self.current_level == 2:
            if self.win_points >= 35:
                self.win_conditions = 'opened'
        if self.current_level == 3:
            if self.win_points >= 58:
                self.win_conditions = 'opened'

        # user interface
        self.change_coins = change_coins

        # coin sound
        self.coin_sounds = [pygame.mixer.Sound(sounds_path + 'pickup-silver.mp3'), pygame.mixer.Sound(sounds_path + 'pickup-gold.wav')]      
        self.monster_explose = pygame.mixer.Sound(sounds_path + 'monster_die.wav')

        # dust setup
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # explosion sprites
        self.explosion_sprites = pygame.sprite.GroupSingle()

        # BG_PALM SETUP
        bg_palm_layout = import_csv_layout(level_data['bg_palm'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg_palm')
        # FG_PALM SETUP
        fg_palm_layout = import_csv_layout(level_data['fg_palm'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg_palm')
        # TERRAIN SETUP
        terrain_layout = import_csv_layout(level_data['Terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'Terrain')
        # GRASS SETUP
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        # COINS SETUP 
        coins_layout = import_csv_layout(level_data['Coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'Coins')
        # # CONSTRAINS SETUP 
        constrains_layout = import_csv_layout(level_data['constrains'])
        self.constrains_sprites = self.create_tile_group(constrains_layout, 'constrains')
        # # ENEMIES SETUP 
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemies_layout, 'enemies')
        # PLAYER SETUP 
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # SHIP SETUP 
        # ship_layout = import_csv_layout(level_data['ship'])
        # self.ship_sprites = self.create_tile_group(ship_layout, 'ship')
        # BRIDGE SETUP 
        # bridge_layout = import_csv_layout(level_data['bridge'])
        # self.bridge_sprites = self.create_tile_group(bridge_layout, 'bridge')

        # WATER SETUP
        water_layout = import_csv_layout(level_data['water'])
        self.water_sprites = self.create_tile_group(water_layout, 'water')
        # WATER_BOT SETUP
        water_bot_layout = import_csv_layout(level_data['water_bot'])
        self.water_bot_sprites = self.create_tile_group(water_bot_layout, 'water_bot')

        # DECORATION
        self.sky = Sky(6)
        level_width = len(terrain_layout[0]) * tile_size
        # self.water = Water(screen_height - 64, level_width)
        self.clouds = Clouds(400, level_width, 4)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'Terrain':
                        terrain_tile_list = import_cut_graphics(path_terrain)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)
                    if type == 'water':
                        # water_tile_list = import_cut_graphics(path_water)
                        # tile_surface = water_tile_list[int(val)]
                        if val == '0': 
                            # water_tile_list = import_cut_graphics(path_water)
                            # tile_surface = water_tile_list[int(val)]
                            # sprite_group.add(sprite)
                            sprite = AnimatedTile(tile_size, x, y, path_water)
                        
                    if type == 'water_bot':
                        if val == '0':
                            water_bot_tile_list = import_cut_graphics_one_file(path_water_bot)
                            tile_surface = water_bot_tile_list[int(val)]
                            sprite = StaticTile(tile_size, x, y, tile_surface)
                            sprite_group.add(sprite)
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics_one_file(path_grass)
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'bg_palm':
                        # bg_palm_tile_list = import_cut_graphics_objects(path_bg_palm)
                        # tile_surface = bg_palm_tile_list[int(val)]
                        if val == '15': sprite = Palm(tile_size, x, y, path_bg_palm_big, 64)
                        if val == '11': sprite = Palm(tile_size, x, y, path_bg_palm_left, 38, -20)
                        if val == '23': sprite = Palm(tile_size, x, y, path_bg_palm_right, 38, 20)
                        if val == '31': sprite = Palm(tile_size, x, y, path_bg_palm_small, 38)
                    if type == 'fg_palm':
                        # fg_palm_tile_list = import_cut_graphics_objects(path_fg_palm)
                        # tile_surface = fg_palm_tile_list[int(val)]
                        if val == '7': sprite = Palm(tile_size, x, y, path_fg_palm_big, 64)
                        if val == '19': sprite = Palm(tile_size, x, y, path_fg_palm_left, 38, - 20)
                        if val == '35': sprite = Palm(tile_size, x, y, path_fg_palm_small, 38)
                        if val == '27': sprite = Palm(tile_size, x, y, path_fg_palm_right, 38, 20)
                    if type == 'Coins':
                        # coins_tile_list = import_cut_graphics_objects(path_coins)
                        # tile_surface = coins_tile_list[int(val)]
                        if val == '0': sprite = Coins(tile_size, x, y, path_coins_g, 3) # StaticTile(tile_size, x, y, tile_surface)
                        if val == '4': sprite = Coins(tile_size, x, y, path_coins_s, 1) # StaticTile(tile_size, x, y, tile_surface)
                    if type == 'constrains':
                        # constrains_tile_list = import_cut_graphics_one_file(path_constrains)
                        # tile_surface = constrains_tile_list[int(val)]
                        sprite = Tile(tile_size, x, y)
                    if type == 'enemies':
                        # enemies_tile_list = import_cut_graphics(path_enemies)
                        # tile_surface = enemies_tile_list[int(val)]
                        # sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite = Enemy(tile_size, x, y)
                    # if type == 'ship':
                    #     sprite = Static_objects(tile_size, x, y)
                    # if type == 'bridge':
                    #     bridge_tile_list = import_cut_graphics_one_file(path_bridge)
                    #     tile_surface = bridge_tile_list[int(val)]
                    #     sprite = StaticTile(tile_size, x, y, tile_surface)
                    sprite_group.add(sprite)
        return sprite_group

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(0, 13)
        else:
            pos += pygame.math.Vector2(0, -13)
        jump_particle_sprite = ParticalEffects(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)


    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
             self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(1, 18)
            else:
                offset = pygame.math.Vector2(-1, 18)
            fall_dust_particle = ParticalEffects(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_widht / 5 and direction_x < 0:
            self.world_shift_x = 6
            player.speed = 0
        elif player_x > screen_widht - (screen_widht / 5) and direction_x > 0:
            self.world_shift_x = -6
            player.speed = 0
        else:
            self.world_shift_x = 0
            player.speed = 6

    def scroll_y(self):
        # player = self.player.sprite
        # player_y = player.rect.centery
        # direction_y = player.direction.y
        # if player_y < screen_height / 8 and direction_y < 0:
        #     self.world_shift_y = 6
        #     player.speed = 0
        # elif player_y > screen_height - (screen_widht / 8):
        #     self.world_shift_y = -6
        #     player.speed = 0
        # else:
        #     self.world_shift_y = 0
        #     player.speed = 6
        pass

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.fg_palm_sprites.sprites()
        for wall in collidable_sprites:
            if wall.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = wall.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = wall.rect.left
                    player.on_right = True
                    self.current_x = player.collision_rect.right
        # if player.on_left and (player.collision_rect.left < self.current_x or player.direction.x >= 0):
        #     player.on_left = False
        # if player.on_right and (player.collision_rect.right > self.current_x or player.direction.x <= 0):
        #     player.on_right = False
    
    def horizontal_palm_collision(self):
        # player = self.player.sprite
        # player.rect.x += player.direction.x * player.speed
        # collidable_sprites = self.fg_palm_sprites.sprites() # pygame.sprite.spritecollide(self.player.sprite, self.fg_palm_sprites, False, pygame.sprite.collide_mask)
        # for palm in collidable_sprites:
        #     if palm.collision_rect.colliderect(player.collision_rect):
        #         if player.direction.x < 0:
        #             player.collision_rect.left = palm.collision_rect.right
        #             player.on_left = True
        #             self.current_x = player.collision_rect.left
        #         elif player.direction.x > 0:
        #             player.collision_rect.right = palm.rcollision_rect.left
        #             player.on_right = True
        #             self.current_x = player.collision_rect.right
        pass

    def vertical_palm_collision(self):                       
        # player = self.player.sprite
        # player.apply_gravity()
        # collidable_sprites = self.fg_palm_sprites.sprites()
        # for top in collidable_sprites:
        #     if top.rect.colliderect(player.collision_rect):
        #         if player.direction.y > 0:
        #             player.collision_rect.bottom = top.collision_rect.top
        #             player.direction.y = 0
        #             player.on_ground = True
        #         elif player.direction.y < 0:
        #             player.collision_rect.top = top.collision_rect.bottom
        #             player.direction.y = 0
        #             player.on_ceiling = True
        # if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
        #     player.on_ground = False
        pass
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.fg_palm_sprites.sprites()
        for floor in collidable_sprites:
            if floor.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = floor.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = floor.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        # if player.on_ceiling and player.direction.y > 0:
        #     player.on_ceiling = False

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constrains_sprites, False):
                enemy.reverse()

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player2((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if val == '1':                    
                    exit_surface = pygame.image.load(path_ship).convert_alpha()
                    sprite = StaticTile(tile_size, x, y + 7, exit_surface)                    
                    self.goal.add(sprite)

    def chek_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def win_cheack(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False) and self.win_conditions == 'opened':
            if self.current_level == 3:
                self.finish_game()
            else:
                self.create_overworld(self.current_level, self.max_new_level)


    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True, pygame.sprite.collide_mask)
        if collided_coins:
            self.coin_sounds[randint(0, 1)].play()
            for coin in collided_coins:
                self.change_coins(coin.value)
                self.win_points += coin.value
                self.player.sprite.heal(coin.value)
            if self.current_level == 0:
                if self.win_points >= 17:
                    self.win_conditions = 'opened'
            if self.current_level == 1:
                if self.win_points >= 27:
                    self.win_conditions = 'opened'
            if self.current_level == 2:
                if self.win_points >= 35:
                    self.win_conditions = 'opened'
            if self.current_level == 3:
                if self.win_points >= 44:
                    self.win_conditions = 'opened'
                    
                    
    def check_enemies_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.monster_explose.play()
                    explosing_sprites = ParticalEffects(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosing_sprites)
                    self.player.sprite.direction.y = -11
                    enemy.kill()
                else:
                    self.player.sprite.direction.y = -3                    
                    self.player.sprite.get_damage()

    def draw(self):
        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift_x, self.world_shift_y)

        # bg_palm draw
        self.bg_palm_sprites.update(self.world_shift_x, self.world_shift_y)
        self.bg_palm_sprites.draw(self.display_surface)


        # dust particle
        self.dust_sprite.update(self.world_shift_x, self.world_shift_y)
        self.dust_sprite.draw(self.display_surface) 
        
        # Terrain draw
        self.terrain_sprites.update(self.world_shift_x, self.world_shift_y)
        self.terrain_sprites.draw(self.display_surface)


        # enemies draw
        self.enemy_sprites.update(self.world_shift_x, self.world_shift_y)        
        self.constrains_sprites.update(self.world_shift_x, self.world_shift_y)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift_x, self.world_shift_y)
        self.explosion_sprites.draw(self.display_surface)

        # coins draw
        self.coins_sprites.update(self.world_shift_x, self.world_shift_y)
        self.coins_sprites.draw(self.display_surface) 
 

        # player draw
        self.player.update()   
        self.horizontal_movement_collision()
        self.get_player_on_ground() 
        self.vertical_movement_collision()
        self.horizontal_palm_collision()
        self.vertical_palm_collision()
        self.scroll_x()
        self.scroll_y()
        self.create_landing_dust()        
        self.player.draw(self.display_surface)
        self.chek_death()
        self.win_cheack() 
        self.check_coin_collisions()
        self.check_enemies_collisions()

        # fg_palm draw
        self.fg_palm_sprites.update(self.world_shift_x, self.world_shift_y)
        self.fg_palm_sprites.draw(self.display_surface)
     


        # constrains draw
        # self.constrains_sprites.draw(self.display_surface)
        # self.constrains_sprites.update(self.world_shift)
        # bridge draw
        # self.bridge_sprites.update(self.world_shift)
        # self.bridge_sprites.draw(self.display_surface)
               
        # Grass draw
        self.grass_sprites.update(self.world_shift_x, self.world_shift_y)
        self.grass_sprites.draw(self.display_surface)
        
        # # ship draw
        # self.ship_sprites.update(self.world_shift)
        # self.ship_sprites.draw(self.display_surface)
        # player goal        
        self.goal.update(self.world_shift_x, self.world_shift_y)
        self.goal.draw(self.display_surface)

        # # water draw
        self.water_sprites.update(self.world_shift_x, self.world_shift_y)
        self.water_sprites.draw(self.display_surface)
               
        # water_bot draw
        self.water_bot_sprites.update(self.world_shift_x, self.world_shift_y)
        self.water_bot_sprites.draw(self.display_surface)
        

        
        