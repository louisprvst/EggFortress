import pygame

class Traps(pygame.sprite.Sprite):
    def __init__(self, x, y, owner):
        super().__init__()
        self.x = x
        self.y = y
        self.is_active = True
        self.owner = owner 

    def can_affect_player(self, player_id):
        """Vérifie si le piège peut affecter ce joueur (pas le propriétaire et piège actif)"""
        return self.is_active and self.owner != player_id

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
