import pygame

import pygame
from entities import Dinosaur

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw(self, game):
        """Dessine l'interface utilisateur avec un design moderne"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Zone de l'UI avec gradient (110 pixels en bas)
        ui_height = 110
        ui_rect = pygame.Rect(0, screen_height - ui_height, screen_width, ui_height)
        
        # Gradient de fond pour l'UI
        for i in range(ui_height):
            alpha = int(200 * (i / ui_height))
            color_top = (25, 25, 35)
            color_bottom = (15, 15, 25)
            
            # Interpolation des couleurs
            factor = i / ui_height
            current_color = tuple(
                int(color_top[j] * (1 - factor) + color_bottom[j] * factor)
                for j in range(3)
            )
            
            pygame.draw.line(self.screen, current_color, 
                           (0, screen_height - ui_height + i), 
                           (screen_width, screen_height - ui_height + i))
        
        # Bordure supérieure brillante
        pygame.draw.line(self.screen, (100, 150, 200), 
                        (0, screen_height - ui_height), 
                        (screen_width, screen_height - ui_height), 3)
        
        # Informations du joueur actuel avec style moderne
        if game.current_player == 1:
            player_color_rgb = (100, 150, 255)
            player_text_display = "Joueur 1 Bleu"
        else:
            player_color_rgb = (255, 100, 100)
            player_text_display = "Joueur 2 Rouge"
        
        # Texte du joueur avec ombre
        player_text = self.font.render(player_text_display, True, player_color_rgb)
        shadow_text = self.font.render(player_text_display, True, (20, 20, 20))
        self.screen.blit(shadow_text, (12, screen_height - 92))
        self.screen.blit(player_text, (10, screen_height - 90))
        
        # Tour avec icône
        turn_text = self.small_font.render(f"Tour: {game.turn_number}", True, (255, 255, 255))
        self.screen.blit(turn_text, (10, screen_height - 55))
        
        # Timer du tour avec couleur dynamique
        elapsed_time = (pygame.time.get_ticks() - game.turn_start_time) / 1000.0
        remaining_time = max(0, game.turn_time_limit - elapsed_time)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        
        # Couleur du timer selon le temps restant
        if remaining_time < 30:
            timer_color = (255, 100, 100)  # Rouge urgent
        elif remaining_time < 60:
            timer_color = (255, 255, 100)  # Jaune attention
        else:
            timer_color = (100, 255, 100)  # Vert normal
            
        timer_text = self.small_font.render(f"Temps: {minutes}:{seconds:02d}", True, timer_color)
        self.screen.blit(timer_text, (130, screen_height - 55))
        
        # Steaks du joueur actuel avec icône et style
        steaks = game.player1_steaks if game.current_player == 1 else game.player2_steaks
        steaks_text = self.small_font.render(f"Steaks: {steaks}", True, (255, 215, 0))
        self.screen.blit(steaks_text, (10, screen_height - 25))
        
        # Boutons avec le nouveau design
        self.draw_spawn_buttons(game, screen_height)
        self.draw_trap_button(game, screen_height)
        
        # Instructions avec style
        self.draw_instructions(screen_width, screen_height)
        
        # Bouton d'attaque si disponible
        self.draw_attack_button(game, screen_height)
        
        # Si le jeu est terminé
        if game.game_over:
            self.draw_game_over(game, screen_width, screen_height)
        
        # Message si le tour va se terminer automatiquement
        if game.spawn_action_done and game.auto_end_turn_time:
            remaining = max(0, (game.auto_end_turn_time - pygame.time.get_ticks()) / 1000.0)
            if remaining > 0:
                msg_text = self.small_font.render("Tour terminé dans {:.1f}s...".format(remaining), True, (255, 255, 0))
                msg_rect = msg_text.get_rect(center=(screen_width//2, 30))
                # Fond semi-transparent moderne
                bg_rect = msg_rect.copy()
                bg_rect.inflate(20, 10)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(180)
                bg_surface.fill((0, 0, 0))
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(msg_text, msg_rect)
        
        # Dessiner les cooldowns au-dessus des œufs
        self.draw_cooldowns(game)
        current_steaks = game.player1_steaks if game.current_player == 1 else game.player2_steaks
        steaks_text = self.small_font.render(f"Steaks: {current_steaks}", True, (255, 255, 255))
        self.screen.blit(steaks_text, (10, screen_height - 30))
        
        # Boutons pour spawner des dinosaures
        self.draw_spawn_buttons(game, screen_height)
        
        # Bouton piège
        self.draw_trap_button(game, screen_height)
        
        # Instructions
        self.draw_instructions(screen_width, screen_height)
        
        # Bouton d'attaque si disponible
        self.draw_attack_button(game, screen_height)
        
        # Si le jeu est terminé
        if game.game_over:
            self.draw_game_over(game, screen_width, screen_height)
        
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
        
        # Dessiner les cooldowns au-dessus des œufs
        self.draw_cooldowns(game)
    
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
            
            # Couleur selon disponibilité avec gradients
            if cooldown > 0:
                # Grisé si en cooldown avec effet de désactivation
                main_color = (80, 80, 80)
                border_color = (60, 60, 60)
                text_color = (150, 150, 150)
            elif current_steaks >= costs[i]:
                # Vert avec gradient si disponible
                main_color = (34, 139, 34)  # Forest Green
                border_color = (0, 100, 0)  # Dark Green
                text_color = (255, 255, 255)
            else:
                # Rouge avec gradient si pas assez de steaks
                main_color = (178, 34, 34)  # Fire Brick
                border_color = (139, 0, 0)  # Dark Red
                text_color = (255, 255, 255)
            
            # Dessiner le bouton avec effet 3D
            button_rect = pygame.Rect(x, y, width, height)
            
            # Ombre portée
            shadow_rect = button_rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=8)
            
            # Fond principal avec gradient simulé
            pygame.draw.rect(self.screen, main_color, button_rect, border_radius=8)
            
            # Bordure avec effet brillant
            pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=8)
            
            # Effet de brillance en haut
            highlight_rect = pygame.Rect(x + 2, y + 2, width - 4, height // 3)
            highlight_color = tuple(min(255, c + 30) for c in main_color)
            pygame.draw.rect(self.screen, highlight_color, highlight_rect, border_radius=6)
            
            # Texte principal (nom du dinosaure)
            name_text = self.small_font.render(names[i], True, text_color)
            name_rect = name_text.get_rect(center=(x + width//2, y + 20))
            self.screen.blit(name_text, name_rect)
            
            # Coût en steaks avec icône
            cost_text = self.small_font.render(f"Steaks: {costs[i]}", True, text_color)
            cost_rect = cost_text.get_rect(center=(x + width//2, y + 35))
            self.screen.blit(cost_text, cost_rect)
            
            # Description (vitesse de mouvement)
            desc_text = pygame.font.Font(None, 20).render(descriptions[i], True, text_color)
            desc_rect = desc_text.get_rect(center=(x + width//2, y + 50))
            self.screen.blit(desc_text, desc_rect)
            
            # Afficher le cooldown si actif
            if cooldown > 0:
                cooldown_text = pygame.font.Font(None, 24).render(f"{cooldown:.1f}s", True, (255, 255, 0))
                cooldown_rect = cooldown_text.get_rect(center=(x + width//2, y + height - 10))
                
                # Fond semi-transparent pour le cooldown
                bg_surface = pygame.Surface((cooldown_text.get_width() + 10, cooldown_text.get_height() + 4))
                bg_surface.set_alpha(180)
                bg_surface.fill((0, 0, 0))
                self.screen.blit(bg_surface, (cooldown_rect.x - 5, cooldown_rect.y - 2))
                
                self.screen.blit(cooldown_text, cooldown_rect)
    
    def draw_trap_button(self, game, screen_height):
        """Dessine le bouton pour placer des pièges avec un design moderne"""
        current_steaks = game.player1_steaks if game.current_player == 1 else game.player2_steaks
        trap_cost = 20
        
        x = 580
        y = screen_height - 85
        width = 80
        height = 70
        
        # Couleur selon disponibilité
        if current_steaks >= trap_cost:
            main_color = (139, 69, 19)  # Saddle Brown
            border_color = (101, 67, 33)  # Dark Brown
            text_color = (255, 255, 255)
        else:
            main_color = (105, 105, 105)  # Dim Gray
            border_color = (69, 69, 69)  # Dark Gray
            text_color = (169, 169, 169)  # Dark Gray
        
        button_rect = pygame.Rect(x, y, width, height)
        
        # Ombre portée
        shadow_rect = button_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=8)
        
        # Fond principal
        pygame.draw.rect(self.screen, main_color, button_rect, border_radius=8)
        
        # Bordure
        pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=8)
        
        # Effet de brillance
        highlight_rect = pygame.Rect(x + 2, y + 2, width - 4, height // 3)
        highlight_color = tuple(min(255, c + 20) for c in main_color)
        pygame.draw.rect(self.screen, highlight_color, highlight_rect, border_radius=6)
        
        # Icône de piège (simulée avec texte)
        trap_text = pygame.font.Font(None, 24).render("TRAP", True, text_color)
        trap_rect = trap_text.get_rect(center=(x + width//2, y + 20))
        self.screen.blit(trap_text, trap_rect)
        
        # Texte "PIÈGE"
        text = self.small_font.render("PIÈGE", True, text_color)
        text_rect = text.get_rect(center=(x + width//2, y + 35))
        self.screen.blit(text, text_rect)
        
        # Coût
        cost_text = pygame.font.Font(None, 20).render(f"Steaks: {trap_cost}", True, text_color)
        cost_rect = cost_text.get_rect(center=(x + width//2, y + 55))
        self.screen.blit(cost_text, cost_rect)
    
    def draw_attack_button(self, game, screen_height):
        """Dessine le bouton d'attaque avec un design moderne"""
        if not (game.selected_dinosaur and 
                isinstance(game.selected_dinosaur, Dinosaur) and 
                game.selected_dinosaur.player == game.current_player and
                not game.selected_dinosaur.has_moved and
                game.selected_dinosaur.immobilized_turns == 0):
            return
        
        # Calculer les cibles possibles
        targets = game.calculate_attack_targets(game.selected_dinosaur)
        if not targets:
            return
        
        x = 680
        y = screen_height - 85
        width = 90
        height = 70
        
        # Design moderne pour le bouton d'attaque
        main_color = (220, 20, 60)  # Crimson
        border_color = (139, 0, 0)  # Dark Red
        text_color = (255, 255, 255)
        
        button_rect = pygame.Rect(x, y, width, height)
        
        # Ombre portée
        shadow_rect = button_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=8)
        
        # Fond principal avec effet pulsant
        pulse_offset = int(10 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
        pulse_color = tuple(min(255, c + pulse_offset) for c in main_color)
        pygame.draw.rect(self.screen, pulse_color, button_rect, border_radius=8)
        
        # Bordure
        pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=8)
        
        # Effet de brillance
        highlight_rect = pygame.Rect(x + 2, y + 2, width - 4, height // 3)
        highlight_color = tuple(min(255, c + 30) for c in pulse_color)
        pygame.draw.rect(self.screen, highlight_color, highlight_rect, border_radius=6)
        
        # Icône d'épée (simulée)
        sword_text = pygame.font.Font(None, 28).render("ATK", True, text_color)
        sword_rect = sword_text.get_rect(center=(x + width//2, y + 18))
        self.screen.blit(sword_text, sword_rect)
        
        # Texte "ATTAQUE"
        attack_text = self.small_font.render("ATTAQUE", True, text_color)
        attack_rect = attack_text.get_rect(center=(x + width//2, y + 35))
        self.screen.blit(attack_text, attack_rect)
        
        # Nombre de cibles
        target_count = len(targets)
        count_text = pygame.font.Font(None, 20).render(f"{target_count} cible{'s' if target_count > 1 else ''}", True, text_color)
        count_rect = count_text.get_rect(center=(x + width//2, y + 55))
        self.screen.blit(count_text, count_rect)
    
    def draw_instructions(self, screen_width, screen_height):
        """Dessine les instructions"""
        instructions = [
            "Clic: Sélectionner/Déplacer",
            "ESPACE: Finir le tour",
            "ECHAP: Annuler"
        ]
        
        x = screen_width - 250
        for i, instruction in enumerate(instructions):
            y = screen_height - 90 + i * 25
            text = self.small_font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (x, y))
            y = screen_height - 90 + i * 25
            text = self.small_font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (x, y))
    
    def draw_game_over(self, game, screen_width, screen_height):
        """Dessine l'écran de fin de jeu"""
        # Overlay semi-transparent
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Message de victoire
        winner_color = "Bleu" if game.winner == 1 else "Rouge"
        winner_text = self.font.render(f"Le joueur {winner_color} a gagné!", True, (255, 255, 255))
        winner_rect = winner_text.get_rect(center=(screen_width//2, screen_height//2))
        self.screen.blit(winner_text, winner_rect)
        
        restart_text = self.small_font.render("Appuyez sur R pour recommencer", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width//2, screen_height//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
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