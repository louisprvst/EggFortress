import pygame
import math
from entities import Dinosaur

class UI:
    def __init__(self, screen):
        self.screen = screen
        # Polices variées pour une meilleure hiérarchie
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)
        
        # État d'animation pour les effets
        self.animation_time = 0
        self.button_hover_states = {}  # Pour tracker le survol des boutons
    
    def draw(self, game):
        """Dessine l'interface utilisateur avec un design UX moderne et professionnel"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Mise à jour du temps d'animation
        self.animation_time = pygame.time.get_ticks() / 1000.0
        
        # Hauteur de la barre UI (plus haute pour plus d'espace)
        ui_height = 140
        ui_y = screen_height - ui_height
        
        # === FOND MODERNE AVEC GRADIENT ÉLÉGANT ===
        self._draw_ui_background(ui_y, ui_height, screen_width, screen_height)
        
        # === SECTION GAUCHE : INFO JOUEUR + RESSOURCES ===
        self._draw_player_info_section(game, ui_y, screen_height)
        
        # === SECTION CENTRE : BOUTONS D'ACTION ===
        self._draw_action_buttons_section(game, ui_y, screen_width, screen_height)
        
        # === SECTION DROITE : TIMER + CONTRÔLES ===
        self._draw_timer_section(game, ui_y, screen_width, screen_height)
        
        # === BOUTON D'ATTAQUE (SI DISPONIBLE) ===
        if self._should_show_attack_button(game):
            self._draw_attack_button(game, ui_y, screen_width)
        
        # === OVERLAYS ET MESSAGES ===
        self._draw_overlays(game, screen_width, screen_height)
        
        # Dessiner les cooldowns au-dessus des œufs
        self.draw_cooldowns(game)
    
    def _draw_ui_background(self, ui_y, ui_height, screen_width, screen_height):
        """Dessine le fond moderne de l'UI avec gradient et effets"""
        # Gradient principal (foncé vers très foncé)
        for i in range(ui_height):
            progress = i / ui_height
            # Gradient de bleu-gris foncé
            r = int(20 + 15 * (1 - progress))
            g = int(25 + 20 * (1 - progress))
            b = int(40 + 25 * (1 - progress))
            
            pygame.draw.line(self.screen, (r, g, b),
                           (0, ui_y + i),
                           (screen_width, ui_y + i))
        
        # Bordure supérieure avec effet lumineux
        pygame.draw.line(self.screen, (80, 120, 180), (0, ui_y), (screen_width, ui_y), 4)
        pygame.draw.line(self.screen, (120, 160, 220), (0, ui_y + 1), (screen_width, ui_y + 1), 2)
        
        # Lignes de séparation subtiles entre sections
        separator_x1 = 380
        separator_x2 = screen_width - 320
        separator_color = (60, 80, 120, 100)
        
        for x in [separator_x1, separator_x2]:
            pygame.draw.line(self.screen, separator_color, (x, ui_y + 10), (x, ui_y + ui_height - 10), 2)
    
    def _draw_player_info_section(self, game, ui_y, screen_height):
        """Section gauche : informations du joueur et ressources"""
        section_x = 20
        section_y = ui_y + 15
        
        # Couleur du joueur actuel
        if game.current_player == 1:
            player_color = (100, 180, 255)
            player_name = "JOUEUR 1"
        else:
            player_color = (255, 100, 120)
            player_name = "JOUEUR 2"
        
        # Nom du joueur
        player_text = self.font.render(player_name, True, player_color)
        shadow_text = self.font.render(player_name, True, (0, 0, 0))
        self.screen.blit(shadow_text, (section_x + 2, section_y + 2))
        self.screen.blit(player_text, (section_x, section_y))
        
        # Numéro du tour avec style
        turn_y = section_y + 40
        turn_label = self.small_font.render("Tour", True, (150, 150, 180))
        turn_number = self.medium_font.render(f"#{game.turn_number}", True, (255, 255, 255))
        self.screen.blit(turn_label, (section_x, turn_y))
        self.screen.blit(turn_number, (section_x + 60, turn_y - 2))
        
        # Steaks avec icône stylée
        steaks_y = section_y + 75
        steaks = game.player1_steaks if game.current_player == 1 else game.player2_steaks
        self._draw_steak_display(section_x, steaks_y, steaks)
    
    def _draw_steak_display(self, x, y, amount):
        """Affiche les steaks avec une icône personnalisée et animation"""
        # Icône de viande (rectangle arrondi avec détails)
        icon_size = 32
        icon_rect = pygame.Rect(x, y, icon_size, icon_size)
        
        # Fond de l'icône
        pygame.draw.rect(self.screen, (139, 69, 19), icon_rect, border_radius=6)
        pygame.draw.rect(self.screen, (205, 133, 63), icon_rect.inflate(-8, -8), border_radius=4)
        
        # Détails de viande (lignes blanches)
        pygame.draw.line(self.screen, (255, 220, 220), (x + 8, y + 12), (x + 24, y + 12), 2)
        pygame.draw.line(self.screen, (255, 220, 220), (x + 8, y + 20), (x + 24, y + 20), 2)
        
        # Bordure brillante
        pygame.draw.rect(self.screen, (255, 200, 100), icon_rect, 2, border_radius=6)
        
        # Texte du montant avec effet doré
        amount_text = self.font.render(str(amount), True, (255, 215, 0))
        shadow = self.font.render(str(amount), True, (139, 90, 0))
        self.screen.blit(shadow, (x + icon_size + 12, y + 2))
        self.screen.blit(amount_text, (x + icon_size + 10, y))
        
        # Label "Steaks"
        label = self.tiny_font.render("steaks", True, (180, 180, 180))
        self.screen.blit(label, (x + icon_size + 10, y + 30))
    
    def _draw_action_buttons_section(self, game, ui_y, screen_width, screen_height):
        """Section centrale : boutons d'action pour spawner dinosaures et pièges"""
        # Centrer les boutons
        button_spacing = 125
        total_width = button_spacing * 4  # 3 dinos + 1 piège
        start_x = (screen_width - total_width) // 2 + 50
        button_y = ui_y + 20
        
        # Boutons dinosaures
        current_steaks = game.player1_steaks if game.current_player == 1 else game.player2_steaks
        dino_configs = [
            {"type": 1, "name": "RAPIDE", "cost": 40, "stats": "3 Mouv • 30 ATK", "color": (50, 200, 50)},
            {"type": 2, "name": "ÉQUILIBRÉ", "cost": 80, "stats": "2 Mouv • 45 ATK", "color": (200, 150, 50)},
            {"type": 3, "name": "TANK", "cost": 100, "stats": "1 Mouv • 60 ATK", "color": (200, 50, 50)}
        ]
        
        for i, config in enumerate(dino_configs):
            btn_x = start_x + i * button_spacing
            cooldown = game.spawn_cooldowns[game.current_player][config["type"]]
            self._draw_dino_button(btn_x, button_y, config, current_steaks, cooldown, game)
        
        # Bouton piège
        trap_x = start_x + 3 * button_spacing
        self._draw_trap_button(trap_x, button_y, current_steaks, game)
    
    def _draw_dino_button(self, x, y, config, current_steaks, cooldown, game):
        """Dessine un bouton de dinosaure moderne avec état visuel clair"""
        width, height = 110, 95
        button_rect = pygame.Rect(x, y, width, height)
        
        # Déterminer l'état du bouton
        is_available = cooldown <= 0 and current_steaks >= config["cost"]
        is_on_cooldown = cooldown > 0
        is_affordable = current_steaks >= config["cost"]
        
        # Couleurs selon l'état
        if is_available:
            bg_color = config["color"]
            border_color = tuple(min(255, c + 50) for c in config["color"])
            text_color = (255, 255, 255)
            alpha = 255
        elif is_on_cooldown:
            bg_color = (60, 60, 70)
            border_color = (80, 80, 90)
            text_color = (150, 150, 160)
            alpha = 200
        else:  # pas assez de steaks
            bg_color = (100, 50, 50)
            border_color = (150, 80, 80)
            text_color = (200, 150, 150)
            alpha = 220
        
        # Surface du bouton avec alpha
        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Ombre portée
        shadow_rect = button_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=10)
        
        # Fond du bouton avec gradient
        pygame.draw.rect(button_surface, (*bg_color, alpha), (0, 0, width, height), border_radius=10)
        
        # Reflet lumineux en haut
        highlight = pygame.Surface((width - 8, height // 3), pygame.SRCALPHA)
        highlight_color = tuple(min(255, c + 40) for c in bg_color)
        pygame.draw.rect(highlight, (*highlight_color, 80), highlight.get_rect(), border_radius=8)
        button_surface.blit(highlight, (4, 4))
        
        self.screen.blit(button_surface, button_rect)
        
        # Bordure avec effet de profondeur
        pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 60), button_rect.inflate(-2, -2), 1, border_radius=9)
        
        # Contenu du bouton
        text_y_offset = 0
        
        # Nom du dinosaure
        name_text = self.tiny_font.render(config["name"], True, text_color)
        name_rect = name_text.get_rect(centerx=x + width//2, top=y + 8)
        self.screen.blit(name_text, name_rect)
        
        # Coût avec icône
        cost_y = y + 28
        cost_text = self.medium_font.render(f"{config['cost']}", True, (255, 215, 0) if is_affordable else (180, 180, 180))
        cost_rect = cost_text.get_rect(centerx=x + width//2, top=cost_y)
        self.screen.blit(cost_text, cost_rect)
        
        # Stats
        stats_text = self.tiny_font.render(config["stats"], True, text_color)
        stats_rect = stats_text.get_rect(centerx=x + width//2, top=y + 55)
        self.screen.blit(stats_text, stats_rect)
        
        # Barre de cooldown circulaire
        if is_on_cooldown:
            self._draw_circular_cooldown(x + width//2, y + height - 15, cooldown, config["type"], game)
        elif not is_affordable:
            # Indicateur "pas assez de steaks"
            lock_text = self.tiny_font.render("Manque", True, (255, 150, 150))
            lock_rect = lock_text.get_rect(centerx=x + width//2, top=y + height - 18)
            self.screen.blit(lock_text, lock_rect)
    
    def _draw_circular_cooldown(self, center_x, center_y, cooldown, dino_type, game):
        """Dessine une barre de cooldown circulaire"""
        radius = 12
        
        # Durées de cooldown maximales
        max_cooldowns = {1: 5, 2: 8, 3: 12}
        max_cooldown = max_cooldowns.get(dino_type, 5)
        
        # Progression (0 à 1)
        progress = 1 - (cooldown / max_cooldown)
        
        # Message si le tour va se terminer automatiquement
        if game.spawn_action_done and game.auto_end_turn_time:
            remaining = max(0, (game.auto_end_turn_time - pygame.time.get_ticks()) / 1000.0)
            if remaining > 0:
                msg_text = self.small_font.render("Tour terminé dans {:.1f}s...".format(remaining), True, (255, 255, 0))
                msg_rect = msg_text.get_rect(center=(screen_width//2, 30))
                # Fond semi-transparent
                bg_rect = msg_rect.copy()
                bg_rect.inflate(20, 10)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(180)
                bg_surface.fill((0, 0, 0))
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(msg_text, msg_rect)
    
    def draw_spawn_buttons(self, game, screen_height):
        """Dessine les boutons pour spawner des dinosaures avec un design moderne"""
        current_steaks = game.player1_steaks if game.current_player == 1 else game.player2_steaks
        costs = [40, 80, 100]
        names = ["Rapide", "Équilibré", "Tank"]
        descriptions = ["3 mouv.", "2 mouv.", "1 mouv."]
        
        for i in range(3):
            x = 200 + i * 120
            y = screen_height - 85
            width = 110
            height = 70
            
            # Vérifier le cooldown
            cooldown = game.spawn_cooldowns[game.current_player][i + 1]
        # Cercle de fond
        pygame.draw.circle(self.screen, (40, 40, 50), (center_x, center_y), radius)
        
        # Arc de progression
        if progress < 1:
            start_angle = -math.pi / 2  # Commence en haut
            end_angle = start_angle + (2 * math.pi * progress)
            
            # Dessiner l'arc
            points = [(center_x, center_y)]
            for angle in [start_angle + i * 0.1 for i in range(int((end_angle - start_angle) / 0.1) + 1)]:
                x = center_x + int(radius * math.cos(angle))
                y = center_y + int(radius * math.sin(angle))
                points.append((x, y))
            
            if len(points) > 2:
                pygame.draw.polygon(self.screen, (100, 200, 255), points)
        
        # Bordure
        pygame.draw.circle(self.screen, (150, 150, 180), (center_x, center_y), radius, 2)
        
        # Temps restant
        time_text = self.tiny_font.render(f"{int(cooldown)}s", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(center_x, center_y))
        self.screen.blit(time_text, time_rect)
    
    def _draw_trap_button(self, x, y, current_steaks, game):
        """Dessine le bouton de piège"""
        width, height = 110, 95
        trap_cost = 20
        button_rect = pygame.Rect(x, y, width, height)
        
        is_available = current_steaks >= trap_cost
        
        if is_available:
            bg_color = (139, 90, 43)
            border_color = (180, 120, 60)
            text_color = (255, 255, 255)
        else:
            bg_color = (80, 70, 60)
            border_color = (100, 90, 80)
            text_color = (150, 150, 150)
        
        # Ombre
        shadow_rect = button_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=10)
        
        # Fond
        pygame.draw.rect(self.screen, bg_color, button_rect, border_radius=10)
        
        # Reflet
        highlight_rect = pygame.Rect(x + 4, y + 4, width - 8, height // 3)
        highlight_color = tuple(min(255, c + 30) for c in bg_color)
        pygame.draw.rect(self.screen, highlight_color, highlight_rect, border_radius=8)
        
        # Bordure
        pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=10)
        
        # Icône de piège (triangle d'avertissement stylisé)
        icon_text = self.font.render("!", True, (255, 200, 0))
        icon_rect = icon_text.get_rect(centerx=x + width//2, top=y + 8)
        self.screen.blit(icon_text, icon_rect)
        
        # Label
        label_text = self.tiny_font.render("PIÈGE", True, text_color)
        label_rect = label_text.get_rect(centerx=x + width//2, top=y + 40)
        self.screen.blit(label_text, label_rect)
        
        # Coût
        cost_text = self.medium_font.render(f"{trap_cost}", True, (255, 215, 0) if is_available else text_color)
        cost_rect = cost_text.get_rect(centerx=x + width//2, top=y + 60)
        self.screen.blit(cost_text, cost_rect)
    
    def _draw_timer_section(self, game, ui_y, screen_width, screen_height):
        """Section droite : timer avec arc de progression"""
        section_x = screen_width - 280
        section_y = ui_y + 20
        
        # Calculer le temps restant
        elapsed_time = (pygame.time.get_ticks() - game.turn_start_time) / 1000.0
        remaining_time = max(0, game.turn_time_limit - elapsed_time)
        progress = remaining_time / game.turn_time_limit
        
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        
        # Couleur selon le temps restant
        if remaining_time < 30:
            timer_color = (255, 80, 80)
            pulse = abs(math.sin(self.animation_time * 4)) * 0.3 + 0.7
        elif remaining_time < 60:
            timer_color = (255, 200, 80)
            pulse = abs(math.sin(self.animation_time * 2)) * 0.2 + 0.8
        else:
            timer_color = (80, 255, 150)
            pulse = 1.0
        
        # Timer circulaire
        center_x = section_x + 60
        center_y = section_y + 50
        radius = 45
        
        # Cercle de fond
        pygame.draw.circle(self.screen, (30, 35, 50), (center_x, center_y), radius)
        
        # Arc de progression
        if progress > 0:
            start_angle = -math.pi / 2
            end_angle = start_angle + (2 * math.pi * progress)
            
            # Dessiner l'arc plein
            points = [(center_x, center_y)]
            num_points = max(3, int(abs(end_angle - start_angle) * radius / 2))
            for i in range(num_points + 1):
                angle = start_angle + (end_angle - start_angle) * i / num_points
                x = center_x + int(radius * math.cos(angle) * pulse)
                y = center_y + int(radius * math.sin(angle) * pulse)
                points.append((x, y))
            
            if len(points) > 2:
                pygame.draw.polygon(self.screen, timer_color, points)
        
        # Bordure brillante
        pygame.draw.circle(self.screen, tuple(int(c * pulse) for c in timer_color), 
                          (center_x, center_y), radius, 4)
        pygame.draw.circle(self.screen, (255, 255, 255, 100), 
                          (center_x, center_y), radius - 2, 2)
        
        # Temps au centre
        time_text = self.medium_font.render(f"{minutes}:{seconds:02d}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(center_x, center_y))
        self.screen.blit(time_text, time_rect)
        
        # Label "TEMPS"
        label = self.tiny_font.render("TEMPS RESTANT", True, (180, 180, 200))
        label_rect = label.get_rect(centerx=center_x, top=section_y + 105)
        self.screen.blit(label, label_rect)
        
        # Instructions compactes à droite du timer
        instructions = [
            ("ESPACE", "Fin tour"),
            ("ÉCHAP", "Annuler")
        ]
        
        instr_x = section_x + 140
        instr_y = section_y + 25
        
        for i, (key, action) in enumerate(instructions):
            y = instr_y + i * 30
            
            # Touche avec fond
            key_bg = pygame.Rect(instr_x, y, 65, 22)
            pygame.draw.rect(self.screen, (50, 60, 80), key_bg, border_radius=4)
            pygame.draw.rect(self.screen, (100, 120, 150), key_bg, 2, border_radius=4)
            
            key_text = self.tiny_font.render(key, True, (220, 220, 255))
            key_rect = key_text.get_rect(center=key_bg.center)
            self.screen.blit(key_text, key_rect)
            
            # Action
            action_text = self.tiny_font.render(action, True, (180, 180, 200))
            self.screen.blit(action_text, (instr_x + 70, y + 2))
    
    def _should_show_attack_button(self, game):
        """Vérifie si le bouton d'attaque doit être affiché"""
        return (game.selected_dinosaur and 
                isinstance(game.selected_dinosaur, Dinosaur) and 
                game.selected_dinosaur.player == game.current_player and
                not game.selected_dinosaur.has_moved and
                game.selected_dinosaur.immobilized_turns == 0 and
                len(game.calculate_attack_targets(game.selected_dinosaur)) > 0)
    
    def _draw_attack_button(self, game, ui_y, screen_width):
        """Dessine le bouton d'attaque flottant"""
        width, height = 120, 60
        x = (screen_width - width) // 2
        y = ui_y - height - 20  # Au-dessus de la barre UI
        
        button_rect = pygame.Rect(x, y, width, height)
        
        # Effet de pulsation
        pulse = abs(math.sin(self.animation_time * 3)) * 0.15 + 0.85
        
        # Ombre portée
        shadow = button_rect.copy()
        shadow.x += 5
        shadow.y += 5
        pygame.draw.rect(self.screen, (0, 0, 0, 150), shadow, border_radius=12)
        
        # Fond rouge pulsant
        bg_color = (220, 40, 60)
        scaled_color = tuple(int(c * pulse) for c in bg_color)
        pygame.draw.rect(self.screen, scaled_color, button_rect, border_radius=12)
        
        # Bordure lumineuse
        pygame.draw.rect(self.screen, (255, 100, 120), button_rect, 4, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255, 150), button_rect.inflate(-4, -4), 2, border_radius=10)
        
        # Icône épée (X stylisé pour attaque)
        sword_text = self.font.render("X", True, (255, 255, 255))
        sword_rect = sword_text.get_rect(center=(x + width//2, y + 18))
        self.screen.blit(sword_text, sword_rect)
        
        # Texte "ATTAQUER"
        attack_text = self.small_font.render("ATTAQUER", True, (255, 255, 255))
        attack_rect = attack_text.get_rect(center=(x + width//2, y + height - 15))
        self.screen.blit(attack_text, attack_rect)
    
    def _draw_overlays(self, game, screen_width, screen_height):
        """Dessine les overlays (game over, messages temporaires, etc.)"""
        # Game over
        if game.game_over:
            self.draw_game_over(game, screen_width, screen_height)
            return
        
        # Message de fin de tour automatique
        if game.spawn_action_done and game.auto_end_turn_time:
            remaining = max(0, (game.auto_end_turn_time - pygame.time.get_ticks()) / 1000.0)
            if remaining > 0:
                self._draw_auto_end_message(remaining, screen_width)
    
    def _draw_auto_end_message(self, remaining, screen_width):
        """Message de fin de tour automatique"""
        msg_text = self.medium_font.render(f"Tour terminé dans {remaining:.1f}s...", True, (255, 255, 100))
        msg_rect = msg_text.get_rect(center=(screen_width//2, 40))
        
        # Fond avec bordure
        bg_rect = msg_rect.inflate(30, 15)
        pygame.draw.rect(self.screen, (40, 40, 50, 220), bg_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 100), bg_rect, 3, border_radius=8)
        
        self.screen.blit(msg_text, msg_rect)
    
    def draw_game_over(self, game, screen_width, screen_height):
        """Écran de game over élégant"""
        # Overlay sombre
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Panneau central
        panel_width, panel_height = 500, 300
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Fond du panneau avec gradient
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        for i in range(panel_height):
            alpha = 240
            r = 30 + int(20 * i / panel_height)
            g = 35 + int(25 * i / panel_height)
            b = 50 + int(30 * i / panel_height)
            pygame.draw.line(panel_surface, (r, g, b, alpha), (0, i), (panel_width, i))
        
        self.screen.blit(panel_surface, panel_rect)
        
        # Bordure brillante
        winner_color = (100, 180, 255) if game.winner == 1 else (255, 100, 120)
        pygame.draw.rect(self.screen, winner_color, panel_rect, 5, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), panel_rect.inflate(-4, -4), 2, border_radius=14)
        
        # Texte de victoire
        winner_name = "JOUEUR 1 (BLEU)" if game.winner == 1 else "JOUEUR 2 (ROUGE)"
        title_text = self.title_font.render("VICTOIRE !", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=screen_width//2, top=panel_y + 40)
        
        # Ombre du titre
        title_shadow = self.title_font.render("VICTOIRE !", True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Nom du gagnant
        winner_text = self.font.render(winner_name, True, winner_color)
        winner_rect = winner_text.get_rect(center=(screen_width//2, panel_y + 120))
        winner_shadow = self.font.render(winner_name, True, (0, 0, 0))
        winner_shadow_rect = winner_rect.copy()
        winner_shadow_rect.x += 2
        winner_shadow_rect.y += 2
        self.screen.blit(winner_shadow, winner_shadow_rect)
        self.screen.blit(winner_text, winner_rect)
        
        restart_text = self.small_font.render("Appuyez sur R pour recommencer", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width//2, screen_height//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        # Instructions pour rejouer
        restart_text = self.medium_font.render("Appuyez sur [R] pour rejouer", True, (200, 200, 220))
        restart_rect = restart_text.get_rect(center=(screen_width//2, panel_y + 200))
        self.screen.blit(restart_text, restart_rect)
        
        # Effet de pulsation sur la touche R
        pulse = abs(math.sin(self.animation_time * 2)) * 0.3 + 0.7
        r_color = tuple(int(255 * pulse) for _ in range(3))
        r_text = self.font.render("R", True, r_color)
        # Trouver où est le R dans le texte et le surligner
        r_x = restart_rect.left + 140
        r_bg = pygame.Rect(r_x - 5, restart_rect.top - 3, 30, 30)
        pygame.draw.rect(self.screen, (60, 70, 90), r_bg, border_radius=5)
        pygame.draw.rect(self.screen, r_color, r_bg, 2, border_radius=5)
    
    # Conserver les anciennes méthodes pour compatibilité (supprimer les doublons ci-dessous)
    def draw_spawn_buttons(self, game, screen_height):
        """Méthode héritée - redirige vers la nouvelle implémentation"""
        pass  # Déjà géré dans _draw_action_buttons_section
    
    def draw_trap_button(self, game, screen_height):
        """Méthode héritée - redirige vers la nouvelle implémentation"""
        pass  # Déjà géré dans _draw_action_buttons_section
    
    def draw_attack_button(self, game, screen_height):
        """Méthode héritée - redirige vers la nouvelle implémentation"""
        pass  # Déjà géré dans _draw_attack_button
    
    def draw_instructions(self, screen_width, screen_height):
        """Méthode héritée - redirige vers la nouvelle implémentation"""
        pass  # Déjà géré dans _draw_timer_section
    
    def draw_cooldowns(self, game):
        """Dessine les cooldowns au-dessus des œufs"""
        for player_id, egg in game.eggs.items():
            cooldowns = game.spawn_cooldowns[player_id]
            
            # Position au-dessus de l'œuf
            x = egg.x * game.cell_width + game.cell_width // 2
            y = egg.y * game.cell_height - 60
            
            # Afficher chaque cooldown actif
            active_cooldowns = []
            for dino_type in [1, 2, 3]:
                cooldown = cooldowns[dino_type]
                if cooldown > 0:
                    dino_names = {1: "Petit", 2: "Moyen", 3: "Grand"}
                    active_cooldowns.append(f"{dino_names[dino_type]}: {int(cooldown)}s")
            
            # Dessiner les cooldowns
            for i, cooldown_text in enumerate(active_cooldowns):
                color = (255, 100, 100) if player_id == 1 else (100, 100, 255)
                text_surface = self.small_font.render(cooldown_text, True, color)
                text_rect = text_surface.get_rect(center=(x, y - i * 20))
                
                # Fond semi-transparent
                bg_rect = text_rect.copy()
                bg_rect.inflate(10, 4)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(180)
                bg_surface.fill((0, 0, 0))
                self.screen.blit(bg_surface, bg_rect)
                
                # Texte
                self.screen.blit(text_surface, text_rect)
