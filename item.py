import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, asset_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(asset_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        pass