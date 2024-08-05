import pygame
import random

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image1 = pygame.image.load("./assets/bomb1.png").convert_alpha()
        self.image2 = pygame.image.load("./assets/bomb2.png").convert_alpha()
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = -512 # out of screen
        self.rect.y = -512
        self.direction = 0
        self.exploded = False

    def hide(self):
        self.rect.x = -512 # out of screen
        self.rect.y = -512

    def update(self):
        self.frame = self.frame + 1
        if self.frame > 1:
            self.frame = 0
        if self.frame==0:
            self.image = self.image1
        if self.frame==1:
            self.image = self.image2
        if self.exploded:
            self.hide()
        pass