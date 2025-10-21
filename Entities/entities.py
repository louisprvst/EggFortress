import pygame
import math

class Entity:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player  # 1 pour bleu, 2 pour rouge
        self.image = None
    
    def draw(self, screen, cell_width, cell_height):
        if self.image:
            screen.blit(self.image, (self.x * cell_width, self.y * cell_height))