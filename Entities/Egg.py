import pygame
from Entities.entities import Entity

class Egg(Entity):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.max_health = 100
        self.health = self.max_health
        self.load_image()
    
    def load_image(self):
        """Charge l'image de l'œuf selon le joueur - utilise les œufs de base"""
        try:
            # Utiliser les œufs de base pour les œufs principaux
            if self.player == 1:
                filename = "assets/images/Eggs/base_water_egg.png"  # Bleu = eau
            else:
                filename = "assets/images/Eggs/base_fire_egg.png"   # Rouge = feu
            
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, (60, 75))  # Plus gros pour les œufs principaux
        except:
            # Image de secours
            self.image = pygame.Surface((60, 75))
            color = (100, 150, 255) if self.player == 1 else (255, 100, 100)
            self.image.fill(color)
    
    def take_damage(self, damage):
        """L'œuf prend des dégâts"""
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.load_dead_image()
    
    def load_dead_image(self):
        """Charge l'image de l'œuf mort - utilise les œufs de base cassés"""
        try:
            # Utiliser les œufs de base cassés
            if self.player == 1:
                filename = "assets/images/Eggs/base_broken_water_egg.png"  # Bleu = eau cassée
            else:
                filename = "assets/images/Eggs/base_broken_fire_egg.png"   # Rouge = feu cassé
            
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, (60, 75))
        except:
            # Image de secours
            self.image = pygame.Surface((60, 75))
            self.image.fill((100, 100, 100))
    
    def draw(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine l'œuf avec sa barre de vie pixel art (supporte offsets de plateau)"""
        # Calculer la position en tenant compte des offsets du plateau
        x_pos = self.x * cell_width + board_offset_x
        y_pos = self.y * cell_height + board_offset_y

        # Dessiner l'œuf
        if self.image:
            screen.blit(self.image, (x_pos, y_pos))

        # Dessiner la barre de vie avec les assets pixel art
        self.draw_health_bar_pixelart(screen, cell_width, cell_height, board_offset_x, board_offset_y)
    
    def draw_health_bar_pixelart(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine la barre de vie avec les images pixel art des assets (supporte offsets)"""
        health_ratio = self.health / self.max_health
        health_percentage = int(health_ratio * 10) * 10  # Arrondir à la dizaine
        
        try:
            # Charger l'image de barre de vie correspondante
            health_bar_image = pygame.image.load(f"assets/images/LifeBars/{health_percentage}%.png")
            health_bar_image = pygame.transform.scale(health_bar_image, (cell_width - 10, 12))
            
            # Position de la barre de vie avec offsets
            bar_x = self.x * cell_width + 5 + board_offset_x
            bar_y = self.y * cell_height - 18 + board_offset_y
            
            screen.blit(health_bar_image, (bar_x, bar_y))
            
        except:
            # Fallback vers l'ancienne méthode si les images ne sont pas trouvées
            bar_width = cell_width - 10
            bar_height = 8
            bar_x = self.x * cell_width + 5 + board_offset_x
            bar_y = self.y * cell_height - 15 + board_offset_y
            
            # Fond de la barre
            pygame.draw.rect(screen, (100, 100, 100), 
                            (bar_x, bar_y, bar_width, bar_height))
            
            # Barre de vie
            health_width = int(bar_width * health_ratio)
            color = (255, 0, 0) if health_ratio < 0.3 else (255, 255, 0) if health_ratio < 0.7 else (0, 255, 0)
            pygame.draw.rect(screen, color, 
                            (bar_x, bar_y, health_width, bar_height))