#####################################################################
# " T h E   M a Z e "
# Another tiny 2d game made with python and pygame
# Code and artwork by fabrice.kauffmann@gmail.com
#
# History:
# 2024.07.15 - initial version inspired from programmez.com
# 2024.07.19 - disable player moves if game paused
# 2024.07.21 - random items location
# 2024.07.22 - random player start location
# 2024.07.23 - external map files support
# 2024.07.24 - code refactoring
# 2024.07.25 - more sounds added
# 2024.07.27 - bonus timme added
# 2024.07.31 - monster added
# 2024.08.06 - fixed check of map boundaries
#
# To Do:
# - check if no more space available to spawn objects ✔️
# - initialize array with numpy ✔️
# - count the number of files in the maps folder ✔️
# - more and better sounds ✔️
# - add random ennemy ✔️
# - compute an display score ✔️
# - add time bonus ✔️
# - reset time and number of items after game over ✔️
# - change window icon and title ✔️ 
# - basic AI logic ✔️
#####################################################################
import pygame
import os
import random
import numpy as np

from wall import Wall
from player import Player
from monster import Monster
from bomb import Bomb
from labyrinth import Labyrinth
from item import Item

# game parameters
DEBUG = False
NUM_MAPS = 1
MAP_HEIGHT = 11
MAP_WIDTH = 20
SCORE = 0
MAX_TIME = 6100
LEVEL_TIME = MAX_TIME
MAX_ITEMS = 10
LEVEL_ITEMS = MAX_ITEMS
TILE_SIZE = 64
BACKGROUND_COLOR = (200, 200, 200)

# create empty map
labyrinth_array = np.zeros((MAP_HEIGHT, MAP_WIDTH))

# create global sprites groups
sprites_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
labyrinth_group = pygame.sprite.Group()

# count the number of maps
def count_maps():
    directory = './maps'
    # Count the number of .txt files using os
    num_txt_files = len([f for f in os.listdir(directory) if f.endswith('.txt')])
    print(f'Number of maps: {num_txt_files}')
    return num_txt_files

# load map from random file
def read_map(array, num_maps):
    idx = random.randint(1,num_maps)
    mapFile = open("./maps/" + str(idx) + ".txt", 'r')
    print("Reading map: " + mapFile.name)
    lines = mapFile.readlines()
    row = 0
    for line in lines:
        line = line.strip()
        for x in range(0, len(line)):
            if line[x]=='X':
                array[row][x]=1
            else:
                array[row][x]=0
        row = row + 1
    mapFile.close()

# generate the maze image and spawn random items
def draw_maze(screen, player, monster):
    global DEBUG
    global NUM_MAPS
    global LEVEL_TIME
    global LEVEL_ITEMS
    global TILE_SIZE
    global BACKGROUND_COLOR

    global labyrinth_array
    global sprites_group
    global item_group
    global labyrinth_group

    screen.fill(BACKGROUND_COLOR)
    item_group.empty()
    labyrinth_group.empty()
    read_map(labyrinth_array, NUM_MAPS)
    labyrinth = Labyrinth(labyrinth_array, 64, 64, LEVEL_ITEMS, player, monster)
    labyrinth.randomize()
    labyrinth.read_and_display(labyrinth_group, item_group)
    labyrinth_group.draw(screen)
    return screen.copy()

# main game loop
def run():
    global DEBUG
    global NUM_MAPS
    global LEVEL_TIME
    global LEVEL_ITEMS
    global TILE_SIZE
    global BACKGROUND_COLOR
    global SCORE

    global labyrinth_array
    global sprites_group
    global item_group
    global labyrinth_group


    # init pygame and mixer
    pygame.init()
    pygame.mixer.init()

    # set window title and icon
    pygame.display.set_caption("T h E   M a Z e")
    icon = pygame.image.load("./assets/diamond.png")
    pygame.display.set_icon(icon)

    # set window size
    screen = pygame.display.set_mode((1280, 700))
    screen.fill(BACKGROUND_COLOR)


    # local vars
    running = True
    mute_sound = False
    countdown = LEVEL_TIME
    countdown_display = ""

    NUM_MAPS = count_maps()
    read_map(labyrinth_array, NUM_MAPS)

    # create sprites
    player = Player()
    monster = Monster()
    bomb = Bomb()

    # add player and monster to sprite group
    sprites_group.add(player, monster, bomb)

    # create the maze image and store it in memory
    labyrinth_background = draw_maze(screen, player, monster)

    # create sound effects
    gamecoin_sound = pygame.mixer.Sound("./assets/gamecoin.ogg")
    gameover_sound = pygame.mixer.Sound("./assets/gameover.ogg")
    youwin_sound = pygame.mixer.Sound("./assets/youwin.ogg")
    explosion_sound = pygame.mixer.Sound("./assets/explosion.wav")

    # create fonts
    game_font_chrono = pygame.freetype.Font("./assets/SuperMario256.ttf", 40)
    game_font_win_lost = pygame.freetype.Font("./assets/SuperMario256.ttf", 140)

    # create user event
    clock_event = pygame.USEREVENT + 1

    # trigger clock event every 100ms
    pygame.time.set_timer(clock_event, 100)

    # main game loop
    while running:
        pygame.time.Clock().tick(12)

        # loop on events
        for event in pygame.event.get():
            # check if ESC pressed
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
            # update count down
            if event.type == clock_event and countdown >= 0 and len(item_group) > 0:
                monster.move(TILE_SIZE, labyrinth_array, player)
                countdown -= 10
                countdown_second = int(countdown/100)
                countdown_display = str(countdown_second).zfill(2)

        # capture player keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if countdown>0 and len(item_group)>0:
                player.move_left(TILE_SIZE)
        elif keys[pygame.K_UP]:
            if countdown>0 and len(item_group)>0:
                player.move_up(TILE_SIZE)
        elif keys[pygame.K_DOWN]:
            if countdown>0 and len(item_group)>0:
                player.move_down(TILE_SIZE)
        elif keys[pygame.K_RIGHT]:
            if countdown>0 and len(item_group)>0:
                player.move_right(TILE_SIZE)
        elif keys[pygame.K_x]:
            if not monster.killed:
                bomb.exploded = False
                bomb.rect.x = player.rect.x
                bomb.rect.y = player.rect.y        
        elif keys[pygame.K_SPACE]:
            # restart the game or increase the difficulty
            # (more items and less time)
            if countdown<=0 or len(item_group)==0 or DEBUG:
                # decrease time and icnrease number of items
                if len(item_group) == 0:
                    if (LEVEL_TIME > 1100):
                        LEVEL_TIME = LEVEL_TIME - 100
                    LEVEL_ITEMS = LEVEL_ITEMS + 1
                else:
                    # reset time and max number of items
                    LEVEL_ITEMS = MAX_ITEMS
                    LEVEL_TIME = MAX_TIME
                    SCORE = 0                    
                countdown = LEVEL_TIME
                monster.killed = False
                bomb.exloded = False
                bomb.hide()
                labyrinth_background = draw_maze(screen, player, monster)
                mute_sound = False

        # check map boundaries
        if player.rect.x/64 < 0 or player.rect.x/64>=MAP_WIDTH or player.rect.y/64 < 0 or player.rect.y/64>=MAP_HEIGHT:
            player.move_rewind(TILE_SIZE)    
        
        # check collisions with walls
        if labyrinth_array[int(player.rect.y/64)][int(player.rect.x/64)] == 1:
            player.move_rewind(TILE_SIZE)

        # check collisions with time bonus
        if labyrinth_array[int(player.rect.y/64)][int(player.rect.x/64)] == 4:
            labyrinth_array[int(player.rect.y/64)][int(player.rect.x/64)] = 0
            countdown = LEVEL_TIME
            youwin_sound.play()
        
        # check collision with monster
        if player.rect.x==monster.rect.x and player.rect.y==monster.rect.y and not monster.killed:
            countdown = 0

        # check collision with bomb
        if monster.rect.x==bomb.rect.x and monster.rect.y==bomb.rect.y:
            monster.killed = True
            bomb.exploded = True
            explosion_sound.play()

        # draw the maze
        screen.blit(labyrinth_background,(0,0))

        # show sprites groups
        sprites_group.update()
        sprites_group.draw(screen)
        item_group.draw(screen)

        # check if item is collected
        if pygame.sprite.spritecollide(player, item_group, True):
            gamecoin_sound.play()
        

        # no more items ==> YOU WIN
        if len(item_group) == 0 and countdown > 0:
            game_font_win_lost.render_to(screen, (310,300),"YOU WIN", (255,255,0))
            game_font_chrono.render_to(screen, (360,420),"Press SPACE to continue", (255,255,255))
            if not mute_sound:
                youwin_sound.play()
                SCORE = SCORE + 1000
                mute_sound = True

        # no more time ==> YOU LOOSE
        if countdown <= 0:
            game_font_win_lost.render_to(screen, (200,300), "GAME OVER", (255,255,0))      
            game_font_chrono.render_to(screen, (360,420),"Press SPACE to continue", (255,255,255))
            if not mute_sound:
                gameover_sound.play()
                mute_sound = True

        # show the timer
        game_font_chrono.render_to(screen, (10,15), f"TIME: {countdown_display}", (255,255,0)) 

        # show the score
        game_font_chrono.render_to(screen, (10,655), f"SCORE: {SCORE}", (255,255,0)) 

        # show keys
        game_font_chrono.render_to(screen, (965,655), "X=DROP BOMB", (255,255,0))

        pygame.display.flip()

    # quit app
    pygame.quit()

if __name__ == "__main__":
    run()