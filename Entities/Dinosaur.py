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
        except:
            size = 40 + (self.dino_type - 1) * 10
            self.image = pygame.Surface((size, size))
            color = (0, 0, 255) if self.player == 1 else (255, 0, 0)
            self.image.fill(color)
    
    def take_damage(self, damage):
        """Le dinosaure prend des dégâts"""
        self.health = max(0, self.health - damage)
    
    def draw(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine le dinosaure avec sa barre de vie"""
        x_pos = self.x * cell_width + board_offset_x
        y_pos = self.y * cell_height + board_offset_y

        if self.image:
            scaled_image = pygame.transform.scale(self.image, (int(cell_width), int(cell_height)))
            screen.blit(scaled_image, (x_pos, y_pos))

        self.draw_health_bar_pixelart(screen, cell_width, cell_height, board_offset_x, board_offset_y)

        if self.immobilized_turns > 0:
            pygame.draw.rect(screen, (255, 0, 0), 
                           (int(x_pos + 5), int(y_pos + 5), 
                            int(cell_width - 10), int(cell_height - 10)), 3)
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.immobilized_turns), True, (255, 255, 255))
            text_rect = text.get_rect(center=(int(x_pos + cell_width//2), 
                                            int(y_pos + cell_height//2)))
            screen.blit(text, text_rect)
    
    def draw_health_bar_pixelart(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine une barre de vie classique pygame pour les dinosaures"""
        health_ratio = self.health / self.max_health
        
        # Dimensions de la barre
        bar_width = cell_width - 10
        bar_height = 8
        bar_x = self.x * cell_width + 5 + board_offset_x
        bar_y = self.y * cell_height - 12 + board_offset_y
        
        # Fond de la barre (noir)
        pygame.draw.rect(screen, (40, 40, 40), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Barre de vie colorée selon le pourcentage
        health_width = int(bar_width * health_ratio)
        if health_ratio > 0.7:
            color = (0, 255, 0)  # Vert
        elif health_ratio > 0.3:
            color = (255, 255, 0)  # Jaune
        else:
            color = (255, 0, 0)  # Rouge
        
        pygame.draw.rect(screen, color, 
                        (bar_x, bar_y, health_width, bar_height))
        
        # Bordure de la barre (blanche)
        pygame.draw.rect(screen, (255, 255, 255), 
                        (bar_x, bar_y, bar_width, bar_height), 1)