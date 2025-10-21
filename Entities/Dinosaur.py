import pygame
from Entities.entities import Entity

class Dinosaur(Entity):
    def __init__(self, x, y, player, dino_type):
        super().__init__(x, y, player)
        self.dino_type = dino_type  # 1, 2, ou 3
        self.has_moved = False
        self.immobilized_turns = 0  # Tours d'immobilisation restants
        self.setup_stats()
        self.load_image()
    
    def setup_stats(self):
        """Configure les statistiques selon le type de dinosaure"""
        if self.dino_type == 1:
            # Petit et rapide
            self.max_health = 60
            self.attack_power = 30  # Augmenté pour plus d'équilibre
            self.movement_range = 3
        elif self.dino_type == 2:
            # Moyen
            self.max_health = 80
            self.attack_power = 45  # Attaque proportionnelle au prix
            self.movement_range = 2
        else:  # dino_type == 3
            # Gros et lent mais fort
            self.max_health = 120
            self.attack_power = 60  # Plus fort car plus cher
            self.movement_range = 1
        
        self.health = self.max_health
    
    def load_image(self):
        """Charge l'image du dinosaure"""
        try:
            color = "Blue" if self.player == 1 else "Red"
            filename = f"assets/images/Dinos/Dino{self.dino_type}_{color}.png"
            self.image = pygame.image.load(filename)
            
            # Taille selon le type
            if self.dino_type == 1:
                size = (40, 40)
            elif self.dino_type == 2:
                size = (50, 50)
            else:
                size = (60, 60)
            
            self.image = pygame.transform.scale(self.image, size)
        except:
            # Image de secours
            size = 40 + (self.dino_type - 1) * 10
            self.image = pygame.Surface((size, size))
            color = (0, 0, 255) if self.player == 1 else (255, 0, 0)
            self.image.fill(color)
    
    def take_damage(self, damage):
        """Le dinosaure prend des dégâts"""
        self.health = max(0, self.health - damage)
    
    def draw(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine le dinosaure avec sa barre de vie pixel art (supporte offsets)"""
        # Calculer la position en tenant compte des offsets
        x_pos = self.x * cell_width + board_offset_x
        y_pos = self.y * cell_height + board_offset_y

        # Dessiner le dinosaure
        if self.image:
            screen.blit(self.image, (x_pos, y_pos))

        # Dessiner la barre de vie avec pixel art
        self.draw_health_bar_pixelart(screen, cell_width, cell_height, board_offset_x, board_offset_y)

        # Indicateur de mouvement
        if self.has_moved:
            pygame.draw.circle(screen, (128, 128, 128), 
                             (x_pos + cell_width - 10, 
                              y_pos + 10), 5)

        # Indicateur d'immobilisation
        if self.immobilized_turns > 0:
            # Dessiner des chaînes ou un effet visuel
            pygame.draw.rect(screen, (255, 0, 0), 
                           (x_pos + 5, y_pos + 5, 
                            cell_width - 10, cell_height - 10), 3)
            # Afficher le nombre de tours restants
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.immobilized_turns), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x_pos + cell_width//2, 
                                            y_pos + cell_height//2))
            screen.blit(text, text_rect)
    
    def draw_health_bar_pixelart(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine la barre de vie avec les images pixel art des assets (supporte offsets)"""
        health_ratio = self.health / self.max_health
        health_percentage = int(health_ratio * 10) * 10  # Arrondir à la dizaine
        
        try:
            # Charger l'image de barre de vie correspondante
            health_bar_image = pygame.image.load(f"assets/images/LifeBars/{health_percentage}%.png")
            health_bar_image = pygame.transform.scale(health_bar_image, (cell_width - 10, 8))
            
            # Position de la barre de vie avec offsets
            bar_x = self.x * cell_width + 5 + board_offset_x
            bar_y = self.y * cell_height - 15 + board_offset_y
            
            screen.blit(health_bar_image, (bar_x, bar_y))
            
        except:
            # Fallback vers l'ancienne méthode
            bar_width = cell_width - 10
            bar_height = 6
            bar_x = self.x * cell_width + 5 + board_offset_x
            bar_y = self.y * cell_height - 12 + board_offset_y
            
            # Fond de la barre
            pygame.draw.rect(screen, (100, 100, 100), 
                            (bar_x, bar_y, bar_width, bar_height))
            
            # Barre de vie
            health_width = int(bar_width * health_ratio)
            color = (255, 0, 0) if health_ratio < 0.3 else (255, 255, 0) if health_ratio < 0.7 else (0, 255, 0)
            pygame.draw.rect(screen, color, 
                            (bar_x, bar_y, health_width, bar_height))