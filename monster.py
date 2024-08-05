import pygame
import random

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("./assets/gargoyle1.png").convert_alpha()
        self.image2 = pygame.image.load("./assets/gargoyle2.png").convert_alpha()
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = 512
        self.rect.y = 512
        self.direction = 0
        self.killed = False

    def move(self, speed, labyrinth_array, player):
        if self.killed:
            return

        # vertical or horizontal move (or none if > 1)
        horiz = random.randint(0,3)

        monster_y = int(self.rect.y/64)
        monster_x = int(self.rect.x/64)

        if horiz==1:
            # check if the player is on the left or the right of the monster
            if player.rect.x < self.rect.x:
                monster_x = monster_x - 1
            if player.rect.x > self.rect.x:
                monster_x = monster_x + 1        
        if horiz==0:
            # check if the player is above or below the monster
            if player.rect.y < self.rect.y:
                monster_y = monster_y - 1
            if player.rect.y > self.rect.y:
                monster_y = monster_y + 1

        # check game bondaries
        if monster_x < 0:
            monster_x = 0
        if monster_x > len(labyrinth_array[0])-1:
            monster = len(labyrinth_array[0])-1
        if monster_y < 0:
            monster_y = 0
        if monster_y > len(labyrinth_array)-1:
            monster_y = len(labyrinth_array)-1

        # cancel the move is there is a blocking wall there
        if labyrinth_array[monster_y][monster_x]!=1:
            self.rect.x = monster_x * 64
            self.rect.y = monster_y * 64

    def update(self):
        if self.killed:
            self.image = self.image2
        else:
            self.image = self.image1
        pass