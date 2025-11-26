import pygame
import math
from Entities.entities import Entity

class SpawnEgg(Entity):
    def __init__(self, x, y, player, dino_type):
        super().__init__(x, y, player)
        self.dino_type = dino_type
        # Turn-based spawn: nombre de tours requis selon le type
        # Mapping choisi proportionnellement aux anciennes durées (20s->2 tours, 40s->4, 80s->8)
        spawn_turns_map = {1: 2, 2: 4, 3: 8}
        self.spawn_turns_required = spawn_turns_map.get(self.dino_type, 2)
        self.spawn_turns_elapsed = 0
        self.spawn_progress = 0.0  # Pour affichage (ratio)
        self.is_spawning = True  # L'œuf est en cours d'éclosion (attente en tours)
        self.is_hatching = False  # True lorsque l'animation d'éclosion a commencé
        self.hatch_animation_time = 0.0  # Temps d'animation en secondes
        
        # Points de vie = moitié de la vie du dinosaure correspondant
        health_map = {1: 30, 2: 40, 3: 60}  # Moitié de 60, 80, 120
        self.max_health = health_map.get(self.dino_type, 30)
        self.health = self.max_health
        
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
        # Cette méthode est appelée chaque frame par Game.update() avec delta_time.
        # Ici, on ne modifie plus la progression liée au temps réel :
        # - La progression en tours est avancée via on_turn_end()
        # - update_spawn ne met à jour que l'animation d'éclosion (en secondes)
        if not self.is_spawning:
            return

        # Mettre à jour l'animation d'éclosion (si elle a commencé)
        if self.is_hatching:
            self.hatch_animation_time += delta_time
    
    def is_ready_to_hatch(self):
        """Vérifie si l'œuf est prêt à éclore (animation terminée)"""
        return self.is_hatching and self.hatch_animation_time >= 0.5
    
    def take_damage(self, damage):
        """L'œuf de spawn prend des dégâts"""
        self.health = max(0, self.health - damage)
    
    def on_turn_end(self):
        """Appelé par Game.end_turn() : avance d'un tour l'éclosion.
        Si le nombre de tours requis est atteint, démarre l'animation d'éclosion.
        """
        if not self.is_spawning or self.is_hatching:
            return

        self.spawn_turns_elapsed += 1
        # Mettre à jour la progression pour l'affichage (ratio)
        try:
            self.spawn_progress = self.spawn_turns_elapsed / self.spawn_turns_required
        except ZeroDivisionError:
            self.spawn_progress = 1.0

        if self.spawn_turns_elapsed >= self.spawn_turns_required:
            self.spawn_progress = 1.0
            self.is_hatching = True
            self.hatch_animation_time = 0.0
    
    
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
            # Afficher le nombre de tours restants avant éclosion (au centre de la case)
            remaining_turns = max(0, self.spawn_turns_required - self.spawn_turns_elapsed)

            # Petit fond circulaire pour la lisibilité
            radius = 14
            num_x = self.x * cell_width + cell_width - radius - 6 + board_offset_x
            num_y = self.y * cell_height + 6 + board_offset_y
            try:
                pygame.draw.circle(screen, (30, 30, 30), (num_x + radius//2, num_y + radius//2), radius)
            except Exception:
                pass

            # Rendu du nombre
            try:
                font = pygame.font.Font(None, 24)
                text = font.render(str(remaining_turns), True, (255, 255, 255))
                text_rect = text.get_rect(center=(num_x + radius//2, num_y + radius//2))
                # Ombre pour lisibilité
                shadow = font.render(str(remaining_turns), True, (0, 0, 0))
                shadow_rect = shadow.get_rect(center=(text_rect.x + 2, text_rect.y + 2))
                screen.blit(shadow, shadow_rect)
                screen.blit(text, text_rect)
            except Exception:
                # Si problème d'affichage de police, dessiner un simple rectangle et le chiffre en fallback
                try:
                    pygame.draw.rect(screen, (0, 0, 0), (num_x, num_y, radius * 2, radius * 2))
                except Exception:
                    pass
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
        
        # Dessiner la barre de vie
        self.draw_health_bar(screen, cell_width, cell_height, board_offset_x, board_offset_y)
    
    def draw_health_bar(self, screen, cell_width, cell_height, board_offset_x=0, board_offset_y=0):
        """Dessine une barre de vie pour l'œuf de spawn"""
        health_ratio = self.health / self.max_health
        
        # Dimensions de la barre
        bar_width = cell_width - 10
        bar_height = 6
        bar_x = self.x * cell_width + 5 + board_offset_x
        bar_y = self.y * cell_height - 10 + board_offset_y
        
        # Fond de la barre (noir)
        pygame.draw.rect(screen, (40, 40, 40), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Barre de vie colorée selon le pourcentage
        health_width = int(bar_width * health_ratio)
        if health_ratio > 0.7:
            color = (0, 200, 255)  # Cyan pour les œufs
        elif health_ratio > 0.3:
            color = (255, 200, 0)  # Orange
        else:
            color = (255, 0, 0)  # Rouge
        
        pygame.draw.rect(screen, color, 
                        (bar_x, bar_y, health_width, bar_height))
        
        # Bordure blanche
        pygame.draw.rect(screen, (255, 255, 255), 
                        (bar_x, bar_y, bar_width, bar_height), 1)