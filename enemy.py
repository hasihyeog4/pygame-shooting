from typing import Any
import pygame
from pygame.sprite import Group

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = './img/' + color + '.gif'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('./img/boss1.gif').convert_alpha()
        if side == 'right':
            x = screen_width + 50
            self.speed = - 3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft = (x, 80))
    def update(self):
        self.rect.x += self.speed