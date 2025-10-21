import pygame
from Entities.entities import Entity

class Trap(Entity):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.activated = False  # Pour savoir si le piège a déjà été activé
        self.cell_width = None
        self.cell_height = None
        self.load_image()
    
    def load_image(self):
        """Charge l'image du piège - sera redimensionnée lors du dessin"""
        try:
            self.base_image = pygame.image.load("assets/images/Traps/trap.png")
        except:
            # Image de secours
            self.base_image = pygame.Surface((60, 60))
            self.base_image.fill((139, 69, 19))  # Marron
    
    def draw(self, screen, cell_width, cell_height, current_player, board_offset_x=0, board_offset_y=0):
        """Dessine le piège seulement pour le joueur qui l'a placé (supporte offsets)"""
        # Le piège n'est visible que pour le joueur qui l'a placé
        if self.player == current_player and not self.activated:
            # Redimensionner l'image pour qu'elle prenne toute la case
            if self.cell_width != cell_width or self.cell_height != cell_height:
                self.cell_width = cell_width
                self.cell_height = cell_height
                self.image = pygame.transform.scale(self.base_image, (cell_width, cell_height))
            
            # Dessiner le piège en tenant compte des offsets
            x_pos = self.x * cell_width + board_offset_x
            y_pos = self.y * cell_height + board_offset_y
            screen.blit(self.image, (x_pos, y_pos))