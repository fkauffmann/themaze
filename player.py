import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_right = pygame.image.load("./assets/player.png").convert_alpha()
        self.image_left = pygame.transform.flip(self.image_right.copy(), True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect()
        self.rect.x = 512
        self.rect.y = 512
        self.direction = 0

    def update(self):
        pass

    def move_left(self, speed):
        self.rect.x -= speed
        self.direction = 1
        self.image = self.image_left

    def move_right(self, speed):
        self.rect.x += speed
        self.direction = 2
        self.image = self.image_right

    def move_up(self, speed):
        self.rect.y -= speed
        self.direction = 3

    def move_down(self, speed):
        self.rect.y += speed
        self.direction = 4

    def move_rewind(self, speed):
        if self.direction == 1:
            self.rect.x += speed
        elif self.direction == 2:
            self.rect.x -= speed
        elif self.direction == 3:
            self.rect.y += speed
        elif self.direction == 4:
            self.rect.y -= speed