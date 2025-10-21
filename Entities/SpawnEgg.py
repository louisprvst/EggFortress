import pygame
import math
from Entities.entities import Entity

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

    def on_turn_end(self):
        """Called by game.end_turn() to advance spawning per turn.
        Advances the spawn progress by one 'turn' unit (1.0 second equivalent).
        If the egg becomes ready to hatch, it will start the hatching animation.
        """
        # Use 1.0 as a reasonable per-turn time slice to advance spawn progress
        self.update_spawn(1.0)
    
    def draw(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine l'œuf de spawn avec animations (supporte offsets)"""
        center_x = self.x * cell_width + cell_width // 2 + board_offset_x
        center_y = self.y * cell_height + cell_height // 2 + board_offset_y
        
        if not self.is_hatching:
            # Dessiner l'œuf normal avec barre de progression
            if self.image:
                x_pos = self.x * cell_width + board_offset_x
                y_pos = self.y * cell_height + board_offset_y
                screen.blit(self.image, (x_pos, y_pos))
            
            # Barre de progression du spawn
            progress_width = cell_width - 10
            progress_height = 4
            progress_x = self.x * cell_width + 5 + board_offset_x
            progress_y = self.y * cell_height + cell_height - 8 + board_offset_y
            
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