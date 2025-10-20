import pygame
import os
import random
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
    
    def draw(self, screen, cell_width, cell_height):
        """Dessine l'œuf avec sa barre de vie pixel art"""
        super().draw(screen, cell_width, cell_height)
        
        # Dessiner la barre de vie avec les assets pixel art
        self.draw_health_bar_pixelart(screen, cell_width, cell_height)
    
    def draw_health_bar_pixelart(self, screen, cell_width, cell_height):
        """Dessine la barre de vie avec les images pixel art des assets"""
        health_ratio = self.health / self.max_health
        health_percentage = int(health_ratio * 10) * 10  # Arrondir à la dizaine
        
        try:
            # Charger l'image de barre de vie correspondante
            health_bar_image = pygame.image.load(f"assets/images/LifeBars/{health_percentage}%.png")
            health_bar_image = pygame.transform.scale(health_bar_image, (cell_width - 10, 12))
            
            # Position de la barre de vie
            bar_x = self.x * cell_width + 5
            bar_y = self.y * cell_height - 18
            
            screen.blit(health_bar_image, (bar_x, bar_y))
            
        except:
            # Fallback vers l'ancienne méthode si les images ne sont pas trouvées
            bar_width = cell_width - 10
            bar_height = 8
            bar_x = self.x * cell_width + 5
            bar_y = self.y * cell_height - 15
            
            # Fond de la barre
            pygame.draw.rect(screen, (100, 100, 100), 
                            (bar_x, bar_y, bar_width, bar_height))
            
            # Barre de vie
            health_width = int(bar_width * health_ratio)
            color = (255, 0, 0) if health_ratio < 0.3 else (255, 255, 0) if health_ratio < 0.7 else (0, 255, 0)
            pygame.draw.rect(screen, color, 
                            (bar_x, bar_y, health_width, bar_height))

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
    
    def draw(self, screen, cell_width, cell_height):
        """Dessine le dinosaure avec sa barre de vie pixel art"""
        super().draw(screen, cell_width, cell_height)
        
        # Dessiner la barre de vie avec pixel art
        self.draw_health_bar_pixelart(screen, cell_width, cell_height)
        
        # Indicateur de mouvement
        if self.has_moved:
            pygame.draw.circle(screen, (128, 128, 128), 
                             (self.x * cell_width + cell_width - 10, 
                              self.y * cell_height + 10), 5)
        
        # Indicateur d'immobilisation
        if self.immobilized_turns > 0:
            # Dessiner des chaînes ou un effet visuel
            pygame.draw.rect(screen, (255, 0, 0), 
                           (self.x * cell_width + 5, self.y * cell_height + 5, 
                            cell_width - 10, cell_height - 10), 3)
            # Afficher le nombre de tours restants
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.immobilized_turns), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x * cell_width + cell_width//2, 
                                            self.y * cell_height + cell_height//2))
            screen.blit(text, text_rect)
    
    def draw_health_bar_pixelart(self, screen, cell_width, cell_height):
        """Dessine la barre de vie avec les images pixel art des assets"""
        health_ratio = self.health / self.max_health
        health_percentage = int(health_ratio * 10) * 10  # Arrondir à la dizaine
        
        try:
            # Charger l'image de barre de vie correspondante
            health_bar_image = pygame.image.load(f"assets/images/LifeBars/{health_percentage}%.png")
            health_bar_image = pygame.transform.scale(health_bar_image, (cell_width - 10, 8))
            
            # Position de la barre de vie
            bar_x = self.x * cell_width + 5
            bar_y = self.y * cell_height - 15
            
            screen.blit(health_bar_image, (bar_x, bar_y))
            
        except:
            # Fallback vers l'ancienne méthode
            bar_width = cell_width - 10
            bar_height = 6
            bar_x = self.x * cell_width + 5
            bar_y = self.y * cell_height - 12
            
            # Fond de la barre
            pygame.draw.rect(screen, (100, 100, 100), 
                            (bar_x, bar_y, bar_width, bar_height))
            
            # Barre de vie
            health_width = int(bar_width * health_ratio)
            color = (255, 0, 0) if health_ratio < 0.3 else (255, 255, 0) if health_ratio < 0.7 else (0, 255, 0)
            pygame.draw.rect(screen, color, 
                            (bar_x, bar_y, health_width, bar_height))

class SpawnEgg(Entity):
    def __init__(self, x, y, player, dino_type):
        super().__init__(x, y, player)
        self.dino_type = dino_type
        self.spawn_progress = 0.0
        self.is_spawning = True  # L'œuf est en cours d'éclosion
        self.is_hatching = False
        self.hatch_animation_time = 0.0
        self.load_image()
    
    def load_image(self):
        """Charge l'image de l'œuf selon le joueur - utilise les petits œufs pour le spawn"""
        try:
            color = "blue" if self.player == 1 else "red"
            filename = f"assets/images/Eggs/{color}_egg.png"
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, (40, 50))
        except:
            # Image de secours
            self.image = pygame.Surface((40, 50))
            color = (100, 150, 255) if self.player == 1 else (255, 100, 100)
            self.image.fill(color)
    
    def update_spawn(self, delta_time):
        """Met à jour l'animation de spawn"""
        if not self.is_spawning:
            return
            
        # Temps d'éclosion selon le type (en secondes) - comme les cooldowns
        spawn_speeds = {1: 20.0, 2: 40.0, 3: 80.0}
        spawn_duration = spawn_speeds.get(self.dino_type, 20.0)
        
        # Mettre à jour la progression
        self.spawn_progress += delta_time / spawn_duration
        
        # Vérifier si c'est prêt à éclore
        if self.spawn_progress >= 1.0:
            self.spawn_progress = 1.0
            if not self.is_hatching:
                self.is_hatching = True
                self.hatch_animation_time = 0.0
        
        # Mettre à jour l'animation d'éclosion
        if self.is_hatching:
            self.hatch_animation_time += delta_time
    
    def is_ready_to_hatch(self):
        """Vérifie si l'œuf est prêt à éclore (animation terminée)"""
        return self.is_hatching and self.hatch_animation_time >= 0.5
    
    def draw(self, screen, cell_width, cell_height):
        """Dessine l'œuf de spawn avec animations"""
        center_x = self.x * cell_width + cell_width // 2
        center_y = self.y * cell_height + cell_height // 2
        
        if not self.is_hatching:
            # Dessiner l'œuf normal avec barre de progression
            super().draw(screen, cell_width, cell_height)
            
            # Barre de progression du spawn
            progress_width = cell_width - 10
            progress_height = 4
            progress_x = self.x * cell_width + 5
            progress_y = self.y * cell_height + cell_height - 8
            
            # Fond de la barre
            pygame.draw.rect(screen, (100, 100, 100), 
                            (progress_x, progress_y, progress_width, progress_height))
            
            # Barre de progression
            filled_width = int(progress_width * self.spawn_progress)
            color = (0, 255, 0) if self.spawn_progress > 0.8 else (255, 255, 0) if self.spawn_progress > 0.5 else (255, 100, 100)
            pygame.draw.rect(screen, color, 
                            (progress_x, progress_y, filled_width, progress_height))
        else:
            # Animation d'éclosion
            shake_intensity = 5
            shake_x = int(shake_intensity * (self.hatch_animation_time * 10) % 2 - 1)
            shake_y = int(shake_intensity * (self.hatch_animation_time * 8) % 2 - 1)
            
            # Dessiner l'œuf qui tremble
            egg_rect = self.image.get_rect(center=(center_x + shake_x, center_y + shake_y))
            screen.blit(self.image, egg_rect)
            
            # Effets visuels d'éclosion
            if self.hatch_animation_time > 0.2:
                # Étoiles ou particules
                for i in range(8):
                    angle = i * math.pi / 4
                    particle_x = center_x + int(20 * math.cos(angle))
                    particle_y = center_y + int(20 * math.sin(angle))
                    pygame.draw.circle(screen, (255, 255, 0), (particle_x, particle_y), 3)
            
            # Texte "ÉCLOSION!"
            if self.hatch_animation_time > 0.1:
                font = pygame.font.Font(None, 24)
                text = font.render("ÉCLOSION!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(center_x, center_y - 40))
                # Ombre du texte
                shadow_text = font.render("ÉCLOSION!", True, (0, 0, 0))
                screen.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
                screen.blit(text, text_rect)

class Trap(Entity):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.load_image()
    
    def load_image(self):
        """Charge l'image du piège"""
        try:
            self.image = pygame.image.load("assets/images/Traps/trap.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
        except:
            # Image de secours
            self.image = pygame.Surface((30, 30))
            self.image.fill((139, 69, 19))  # Marron