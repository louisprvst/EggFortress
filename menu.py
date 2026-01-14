import pygame
import os
import math
import random
import traceback

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Charger l'image de fond
        self.background_image = None
        try:
            bg_path = "assets/images/background.png"
            if os.path.exists(bg_path):
                self.background_image = pygame.image.load(bg_path)
                # Redimensionner à la taille de l'écran
                self.background_image = pygame.transform.scale(
                    self.background_image, 
                    (self.screen_width, self.screen_height)
                )
        except Exception as e:
            print(f"Impossible de charger l'image de fond: {e}")

        # Charger le logo
        self.logo_image = None
        try:
            logo_path = "assets/images/eggfortress.png"
            if os.path.exists(logo_path):
                logo = pygame.image.load(logo_path).convert_alpha()
                logo_width = 500
                # Calculer la hauteur pour garder les proportions
                aspect_ratio = logo.get_height() / logo.get_width()
                logo_height = int(logo_width * aspect_ratio)
                self.logo_image = pygame.transform.smoothscale(logo, (logo_width, logo_height))
        except Exception as e:
            print(f"Impossible de charger le logo: {e}")

        # Charger le son de clic du menu
        self.click_sound = None
        try:
            self.click_sound = pygame.mixer.Sound("assets/sounds/click-menu.mp3")
        except Exception as e:
            print(f"Impossible de charger le son de clic: {e}")
        
        # Volumes (0.0 à 1.0)
        self.music_volume = 0.3
        self.sfx_volume = 1.0
        
        # Barres de volume
        self.dragging_music = False
        self.dragging_sfx = False
        
        # Appliquer les volumes initiaux
        pygame.mixer.music.set_volume(self.music_volume)
        if self.click_sound:
            self.click_sound.set_volume(self.sfx_volume)
        
        # Polices
        self.title_font = pygame.font.Font(None, 96)
        self.button_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        
        # États du menu
        self.current_screen = "main"  # "main", "game_mode", "map_selection", "settings", "how_to_play"
        self.selected_map = "default"
        self.game_mode = "ai"  # "ai" ou "2players"
        
        # Animation
        self.time = 0
        
        # Boutons
        self.buttons = {
            "play": pygame.Rect(self.screen_width//2 - 150, 400, 300, 80),
            "settings": pygame.Rect(self.screen_width//2 - 150, 500, 300, 80),
            "quit": pygame.Rect(self.screen_width//2 - 150, 600, 300, 80),
            "back": pygame.Rect(50, self.screen_height - 100, 150, 60)
        }
    
    def handle_event(self, event):
        """Gère les événements du menu"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Gestion des barres de volume dans les paramètres
            if self.current_screen == "settings":
                music_slider_rect = pygame.Rect(self.screen_width//2 - 200, 250, 400, 20)
                sfx_slider_rect = pygame.Rect(self.screen_width//2 - 200, 350, 400, 20)
                
                if music_slider_rect.collidepoint(mouse_pos):
                    self.dragging_music = True
                    # Calculer le nouveau volume
                    relative_x = mouse_pos[0] - music_slider_rect.x
                    self.music_volume = max(0.0, min(1.0, relative_x / music_slider_rect.width))
                    pygame.mixer.music.set_volume(self.music_volume)
                elif sfx_slider_rect.collidepoint(mouse_pos):
                    self.dragging_sfx = True
                    # Calculer le nouveau volume
                    relative_x = mouse_pos[0] - sfx_slider_rect.x
                    self.sfx_volume = max(0.0, min(1.0, relative_x / sfx_slider_rect.width))
                    if self.click_sound:
                        self.click_sound.set_volume(self.sfx_volume)
            
            if self.current_screen == "main":
                if self.buttons["play"].collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.current_screen = "game_mode"
                elif self.buttons["settings"].collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.current_screen = "settings"
                elif self.buttons["quit"].collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    return "quit"
            
            elif self.current_screen == "game_mode":
                # Boutons de sélection du mode de jeu
                mode_button_width = 350
                mode_button_height = 250
                spacing = 60
                total_width = mode_button_width * 2 + spacing
                start_x = self.screen_width // 2 - total_width // 2
                
                ai_mode_button = pygame.Rect(start_x, 300, mode_button_width, mode_button_height)
                two_players_button = pygame.Rect(start_x + mode_button_width + spacing, 300, mode_button_width, mode_button_height)
                
                if ai_mode_button.collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.game_mode = "ai"
                    self.current_screen = "map_selection"
                elif two_players_button.collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.game_mode = "2players"
                    self.current_screen = "map_selection"
                elif self.buttons["back"].collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.current_screen = "main"
            
            elif self.current_screen == "map_selection":
                # Boutons de sélection de map
                map_button_width = 250
                map_button_height = 200
                spacing = 40
                total_width = map_button_width * 3 + spacing * 2
                start_x = self.screen_width // 2 - total_width // 2
                
                default_map_button = pygame.Rect(start_x, 300, map_button_width, map_button_height)
                custom_map_button = pygame.Rect(start_x + map_button_width + spacing, 300, map_button_width, map_button_height)
                empty_map_button = pygame.Rect(start_x + (map_button_width + spacing) * 2, 300, map_button_width, map_button_height)
                
                if default_map_button.collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.selected_map = "default"
                    return {"action": "start_game", "map": "default", "game_mode": self.game_mode}
                elif custom_map_button.collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.selected_map = "custom"
                    return {"action": "start_game", "map": "custom", "game_mode": self.game_mode}
                elif empty_map_button.collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.selected_map = "empty"
                    return {"action": "start_game", "map": "empty", "game_mode": self.game_mode}
                elif self.buttons["back"].collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.current_screen = "game_mode"
            
            elif self.current_screen in ["settings", "how_to_play"]:
                if self.buttons["back"].collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.current_screen = "main"
            
            # Bouton "Comment jouer" dans les paramètres
            if self.current_screen == "settings":
                how_to_play_button = pygame.Rect(self.screen_width//2 - 200, 450, 400, 80)
                if how_to_play_button.collidepoint(mouse_pos):
                    if self.click_sound:
                        self.click_sound.play()
                    self.current_screen = "how_to_play"
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_music = False
            self.dragging_sfx = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_music:
                music_slider_rect = pygame.Rect(self.screen_width//2 - 200, 250, 400, 20)
                relative_x = event.pos[0] - music_slider_rect.x
                self.music_volume = max(0.0, min(1.0, relative_x / music_slider_rect.width))
                pygame.mixer.music.set_volume(self.music_volume)
            elif self.dragging_sfx:
                sfx_slider_rect = pygame.Rect(self.screen_width//2 - 200, 350, 400, 20)
                relative_x = event.pos[0] - sfx_slider_rect.x
                self.sfx_volume = max(0.0, min(1.0, relative_x / sfx_slider_rect.width))
                if self.click_sound:
                    self.click_sound.set_volume(self.sfx_volume)
        
        return None
    
    def draw(self):
        """Dessine le menu"""
        if self.current_screen == "main":
            self.draw_main_menu()
        elif self.current_screen == "game_mode":
            self.draw_game_mode_selection()
        elif self.current_screen == "map_selection":
            self.draw_map_selection()
        elif self.current_screen == "settings":
            self.draw_settings()
        elif self.current_screen == "how_to_play":
            self.draw_how_to_play()
    
    def draw_main_menu(self):
        """Dessine le menu principal"""
        # Fond dégradé
        self.draw_background()
        
        # Logo principal
        if self.logo_image:
            logo_rect = self.logo_image.get_rect(center=(self.screen_width//2, 200))
            self.screen.blit(self.logo_image, logo_rect)
        else:
            title_text = self.title_font.render("EGG FORTRESS", True, (255, 255, 255))
            title_shadow = self.title_font.render("EGG FORTRESS", True, (0, 0, 0))
            
            title_rect = title_text.get_rect(center=(self.screen_width//2, 150))
            shadow_rect = title_rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            
            self.screen.blit(title_shadow, shadow_rect)
            self.screen.blit(title_text, title_rect)
        
        # Boutons
        self.draw_button("play", "JOUER", (0, 200, 0), (0, 255, 0))
        self.draw_button("settings", "PARAMÈTRES", (100, 100, 200), (150, 150, 255))
        self.draw_button("quit", "QUITTER", (200, 100, 100), (255, 150, 150))
    
    def draw_game_mode_selection(self):
        """Dessine l'écran de sélection du mode de jeu"""
        # Fond dégradé
        self.draw_background()

        # Titre
        title_text = self.title_font.render("MODE DE JEU", True, (255, 255, 255))
        title_shadow = self.title_font.render("MODE DE JEU", True, (0, 0, 0))
        
        title_rect = title_text.get_rect(center=(self.screen_width//2, 120))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle = self.text_font.render("Choisissez votre mode de jeu :", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen_width//2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Boutons de sélection du mode
        mode_button_width = 350
        mode_button_height = 250
        spacing = 60
        total_width = mode_button_width * 2 + spacing
        start_x = self.screen_width // 2 - total_width // 2
        
        ai_mode_button = pygame.Rect(start_x, 300, mode_button_width, mode_button_height)
        two_players_button = pygame.Rect(start_x + mode_button_width + spacing, 300, mode_button_width, mode_button_height)
        
        mouse_pos = pygame.mouse.get_pos()
        mode_font = pygame.font.Font(None, 50)
        desc_font = pygame.font.Font(None, 28)
        
        # Bouton 1 Joueur
        ai_hover = ai_mode_button.collidepoint(mouse_pos)
        ai_color = (50, 150, 50) if ai_hover else (30, 100, 30)
        pygame.draw.rect(self.screen, ai_color, ai_mode_button, border_radius=15)
        pygame.draw.rect(self.screen, (100, 255, 100), ai_mode_button, 4, border_radius=15)
        
        ai_title = mode_font.render("1 JOUEUR", True, (255, 255, 255))
        ai_title_rect = ai_title.get_rect(center=(ai_mode_button.centerx, ai_mode_button.centery - 20))
        self.screen.blit(ai_title, ai_title_rect)
        
        ai_desc = desc_font.render("Affrontez l'ordinateur", True, (200, 200, 200))
        ai_desc_rect = ai_desc.get_rect(center=(ai_mode_button.centerx, ai_mode_button.centery + 30))
        self.screen.blit(ai_desc, ai_desc_rect)
        
        # Bouton 2 Joueurs
        human_hover = two_players_button.collidepoint(mouse_pos)
        human_color = (150, 50, 50) if human_hover else (100, 30, 30)
        pygame.draw.rect(self.screen, human_color, two_players_button, border_radius=15)
        pygame.draw.rect(self.screen, (255, 100, 100), two_players_button, 4, border_radius=15)
        
        human_title = mode_font.render("2 JOUEURS", True, (255, 255, 255))
        human_title_rect = human_title.get_rect(center=(two_players_button.centerx, two_players_button.centery - 20))
        self.screen.blit(human_title, human_title_rect)
        
        human_desc = desc_font.render("Jouez contre un ami", True, (200, 200, 200))
        human_desc_rect = human_desc.get_rect(center=(two_players_button.centerx, two_players_button.centery + 30))
        self.screen.blit(human_desc, human_desc_rect)
        
        # Bouton retour
        self.draw_button("back", "RETOUR", (100, 100, 100), (150, 150, 150))
    
    def draw_map_selection(self):
        """Dessine l'écran de sélection de map"""
        # Fond dégradé
        self.draw_background()
        
        # Titre
        title_text = self.title_font.render("CHOIX DE LA MAP", True, (255, 255, 255))
        title_shadow = self.title_font.render("CHOIX DE LA MAP", True, (0, 0, 0))
        
        title_rect = title_text.get_rect(center=(self.screen_width//2, 120))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle = self.text_font.render("Sélectionnez une carte pour commencer", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen_width//2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Boutons de sélection de map
        map_button_width = 250
        map_button_height = 200
        spacing = 40
        total_width = map_button_width * 3 + spacing * 2
        start_x = self.screen_width // 2 - total_width // 2
        
        default_map_button = pygame.Rect(start_x, 300, map_button_width, map_button_height)
        custom_map_button = pygame.Rect(start_x + map_button_width + spacing, 300, map_button_width, map_button_height)
        empty_map_button = pygame.Rect(start_x + (map_button_width + spacing) * 2, 300, map_button_width, map_button_height)
        
        mouse_pos = pygame.mouse.get_pos()
        map_name_font = pygame.font.Font(None, 40)
        desc_font = pygame.font.Font(None, 24)
        
        # Bouton Map par défaut (avec obstacles)
        default_hover = default_map_button.collidepoint(mouse_pos)
        default_color = (50, 150, 50) if default_hover else (30, 100, 30)
        pygame.draw.rect(self.screen, default_color, default_map_button, border_radius=15)
        pygame.draw.rect(self.screen, (100, 255, 100), default_map_button, 4, border_radius=15)
        
        default_title = map_name_font.render("PLAINE", True, (255, 255, 255))
        default_title_rect = default_title.get_rect(center=(default_map_button.centerx, default_map_button.y + 35))
        self.screen.blit(default_title, default_title_rect)
        
        desc_lines = ["La plaine sauvage", "classique"]
        for i, line in enumerate(desc_lines):
            desc_text = desc_font.render(line, True, (200, 200, 200))
            desc_rect = desc_text.get_rect(center=(default_map_button.centerx, default_map_button.y + 100 + i * 28))
            self.screen.blit(desc_text, desc_rect)
        
        # Bouton Map personnalisée (labyrinthe)
        custom_hover = custom_map_button.collidepoint(mouse_pos)
        custom_color = (150, 100, 150) if custom_hover else (100, 60, 100)
        pygame.draw.rect(self.screen, custom_color, custom_map_button, border_radius=15)
        pygame.draw.rect(self.screen, (200, 150, 200), custom_map_button, 4, border_radius=15)
        
        custom_title = map_name_font.render("Forêt", True, (255, 255, 255))
        custom_title_rect = custom_title.get_rect(center=(custom_map_button.centerx, custom_map_button.y + 35))
        self.screen.blit(custom_title, custom_title_rect)
        
        custom_desc_lines = ["Les arbres y forment", "un labyrinth"]
        for i, line in enumerate(custom_desc_lines):
            desc_text = desc_font.render(line, True, (200, 200, 200))
            desc_rect = desc_text.get_rect(center=(custom_map_button.centerx, custom_map_button.y + 100 + i * 28))
            self.screen.blit(desc_text, desc_rect)
        
        # Bouton Map vide (que de l'herbe)
        empty_hover = empty_map_button.collidepoint(mouse_pos)
        empty_color = (100, 100, 150) if empty_hover else (60, 60, 100)
        pygame.draw.rect(self.screen, empty_color, empty_map_button, border_radius=15)
        pygame.draw.rect(self.screen, (150, 150, 255), empty_map_button, 4, border_radius=15)
        
        empty_title = map_name_font.render("Terrain vague", True, (255, 255, 255))
        empty_title_rect = empty_title.get_rect(center=(empty_map_button.centerx, empty_map_button.y + 35))
        self.screen.blit(empty_title, empty_title_rect)
        
        empty_desc_lines = ["Le vrai", "no man's land"]
        for i, line in enumerate(empty_desc_lines):
            desc_text = desc_font.render(line, True, (200, 200, 200))
            desc_rect = desc_text.get_rect(center=(empty_map_button.centerx, empty_map_button.y + 100 + i * 28))
            self.screen.blit(desc_text, desc_rect)
        
        # Bouton retour
        self.draw_button("back", "RETOUR", (100, 100, 100), (150, 150, 150))
    
    def draw_settings(self):
        """Dessine le menu des paramètres"""
        self.draw_background()
        
        # Titre
        title = self.title_font.render("PARAMÈTRES", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width//2, 80))
        self.screen.blit(title, title_rect)
        
        # === BARRE DE VOLUME MUSIQUE ===
        music_label = self.button_font.render("Volume Musique", True, (255, 255, 255))
        music_label_rect = music_label.get_rect(center=(self.screen_width//2, 200))
        self.screen.blit(music_label, music_label_rect)
        
        # Barre de fond
        music_slider_rect = pygame.Rect(self.screen_width//2 - 200, 250, 400, 20)
        pygame.draw.rect(self.screen, (60, 60, 60), music_slider_rect, border_radius=10)
        
        # Barre de remplissage
        music_fill_width = int(music_slider_rect.width * self.music_volume)
        music_fill_rect = pygame.Rect(music_slider_rect.x, music_slider_rect.y, music_fill_width, music_slider_rect.height)
        pygame.draw.rect(self.screen, (0, 200, 255), music_fill_rect, border_radius=10)
        
        # Bordure
        pygame.draw.rect(self.screen, (150, 150, 150), music_slider_rect, 2, border_radius=10)
        
        # Pourcentage
        music_percent = self.text_font.render(f"{int(self.music_volume * 100)}%", True, (255, 255, 255))
        music_percent_rect = music_percent.get_rect(center=(self.screen_width//2, 285))
        self.screen.blit(music_percent, music_percent_rect)
        
        # === BARRE DE VOLUME EFFETS SONORES ===
        sfx_label = self.button_font.render("Volume Effets Sonores", True, (255, 255, 255))
        sfx_label_rect = sfx_label.get_rect(center=(self.screen_width//2, 320))
        self.screen.blit(sfx_label, sfx_label_rect)
        
        # Barre de fond
        sfx_slider_rect = pygame.Rect(self.screen_width//2 - 200, 350, 400, 20)
        pygame.draw.rect(self.screen, (60, 60, 60), sfx_slider_rect, border_radius=10)
        
        # Barre de remplissage
        sfx_fill_width = int(sfx_slider_rect.width * self.sfx_volume)
        sfx_fill_rect = pygame.Rect(sfx_slider_rect.x, sfx_slider_rect.y, sfx_fill_width, sfx_slider_rect.height)
        pygame.draw.rect(self.screen, (255, 150, 0), sfx_fill_rect, border_radius=10)
        
        # Bordure
        pygame.draw.rect(self.screen, (150, 150, 150), sfx_slider_rect, 2, border_radius=10)
        
        # Pourcentage
        sfx_percent = self.text_font.render(f"{int(self.sfx_volume * 100)}%", True, (255, 255, 255))
        sfx_percent_rect = sfx_percent.get_rect(center=(self.screen_width//2, 385))
        self.screen.blit(sfx_percent, sfx_percent_rect)
        
        # Bouton Comment jouer (déplacé plus bas)
        how_to_play_button = pygame.Rect(self.screen_width//2 - 200, 450, 400, 80)
        self.draw_custom_button(how_to_play_button, "COMMENT JOUER", (100, 150, 200), (150, 200, 255))
        
        # Informations du jeu
        info_texts = [
            "Version: 1.0",
            "Créé avec Pygame",
            "Jeu de stratégie au tour par tour"
        ]
        
        y_start = 580
        for i, text in enumerate(info_texts):
            info_surface = self.text_font.render(text, True, (200, 200, 200))
            info_rect = info_surface.get_rect(center=(self.screen_width//2, y_start + i * 40))
            self.screen.blit(info_surface, info_rect)
        
        # Bouton retour
        self.draw_button("back", "RETOUR", (150, 150, 150), (200, 200, 200))
    
    def draw_how_to_play(self):
        """Dessine l'écran des règles"""
        self.draw_background()
        
        # Titre
        title = self.title_font.render("COMMENT JOUER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width//2, 80))
        self.screen.blit(title, title_rect)
        
        # Règles et contrôles
        rules = [
            "OBJECTIF:",
            "• Détruire l'œuf ennemi tout en protégeant le vôtre",
            "",
            "CONTRÔLES:",
            "• Clic gauche: Sélectionner/Déplacer dinosaures",
            "• Boutons UI: Spawner dinosaures/pièges", 
            "• ESPACE: Terminer le tour",
            "• ÉCHAP: Annuler l'action",
            "• R: Redémarrer (fin de partie)",
            "",
            "COMBAT:",
            "• Bouton ATTAQUE: Apparaît près des ennemis",
            "• Cliquez pour activer le mode attaque",
            "• Sélectionnez votre cible",
            "",
            "DINOSAURES:",
            "• Type 1 (40 steaks): Rapide, fragile",
            "• Type 2 (80 steaks): Équilibré", 
            "• Type 3 (100 steaks): Lent, résistant",
            "",
            "RESSOURCES:",
            "• +20 steaks par tour",
            "• +20 steaks par ennemi éliminé"
        ]
        
        y_start = 140
        line_height = 25
        
        for i, rule in enumerate(rules):
            if rule in ["OBJECTIF:", "CONTRÔLES:", "COMBAT:", "DINOSAURES:", "RESSOURCES:"]:
                color = (255, 255, 100)  # Jaune pour les titres
                font = self.text_font
            elif rule.startswith("•"):
                color = (200, 200, 200)  # Gris clair pour les points
                font = pygame.font.Font(None, 28)
            else:
                color = (255, 255, 255)  # Blanc pour le texte normal
                font = self.text_font
            
            if rule.strip():  # Ne pas afficher les lignes vides
                text_surface = font.render(rule, True, color)
                text_rect = text_surface.get_rect()
                text_rect.x = 50
                text_rect.y = y_start + i * line_height
                self.screen.blit(text_surface, text_rect)
        
        # Bouton retour
        self.draw_button("back", "RETOUR", (150, 150, 150), (200, 200, 200))
    
    def draw_background(self):
        """Dessine le fond du menu"""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            for y in range(self.screen_height):
                ratio = y / self.screen_height
                r = int(20 * (1 - ratio))
                g = int(30 * (1 - ratio))
                b = int(60 * (1 - ratio))
                pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen_width, y))
    
    def draw_button(self, button_name, text, base_color, hover_color):
        """Dessine un bouton avec effet de survol"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = self.buttons[button_name]
        
        # Couleur selon survol
        if button_rect.collidepoint(mouse_pos):
            color = hover_color
            # Effet de pulsation
            pulse = int(abs(math.sin(self.time * 5)) * 20)
            button_rect = button_rect.inflate(pulse, pulse//2)
        else:
            color = base_color
        
        self.draw_custom_button(button_rect, text, base_color, hover_color)
    
    def draw_custom_button(self, rect, text, base_color, hover_color):
        """Dessine un bouton personnalisé"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Couleur selon survol
        if rect.collidepoint(mouse_pos):
            color = hover_color
        else:
            color = base_color
        
        # Ombre du bouton
        shadow_rect = rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=15)
        
        # Bouton principal
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=15)
        
        # Texte du bouton
        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_shadow = self.button_font.render(text, True, (0, 0, 0))
        
        text_rect = text_surface.get_rect(center=rect.center)
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        
        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text_surface, text_rect)
    
    def draw_game_mode_button(self, button_name, text, base_color, hover_color, selected):
        """Dessine un bouton de mode de jeu avec indication de sélection"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = self.buttons[button_name]
        
        # Couleur selon survol et sélection
        if button_rect.collidepoint(mouse_pos):
            color = hover_color
            # Effet de pulsation si survolé
            pulse = int(abs(math.sin(self.time * 5)) * 10)
            draw_rect = button_rect.inflate(pulse, pulse//2)
        else:
            color = base_color
            draw_rect = button_rect
        
        # Ombre du bouton
        shadow_rect = draw_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=15)
        
        # Bouton principal
        pygame.draw.rect(self.screen, color, draw_rect, border_radius=15)
        
        # Bordure spéciale si sélectionné
        if selected:
            pygame.draw.rect(self.screen, (255, 255, 0), draw_rect, 5, border_radius=15)  # Bordure dorée
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), draw_rect, 3, border_radius=15)
        
        # Texte du bouton - diviser en icône et texte
        lines = text.split(' ', 1)  # Séparer l'icône du texte
        icon = lines[0] if len(lines) > 0 else ""
        label = lines[1] if len(lines) > 1 else ""
        
        # Dessiner l'icône (plus grande)
        icon_font = pygame.font.Font(None, 48)
        icon_surface = icon_font.render(icon, True, (255, 255, 255))
        icon_rect = icon_surface.get_rect(center=(draw_rect.centerx, draw_rect.centery - 15))
        self.screen.blit(icon_surface, icon_rect)
        
        # Dessiner le texte (plus petit)
        text_font = pygame.font.Font(None, 32)
        text_surface = text_font.render(label, True, (255, 255, 255))
        text_shadow = text_font.render(label, True, (0, 0, 0))
        
        text_rect = text_surface.get_rect(center=(draw_rect.centerx, draw_rect.centery + 20))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        
        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text_surface, text_rect)


class MenuManager:
    def __init__(self):
        pygame.init()
        
        # Configuration de l'écran
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("Egg Fortress")
        
        # Menu
        self.menu = MenuScreen(self.screen)
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()
    
    def run(self):
        """Boucle principale du menu"""
        running = True
        
        while running:
            # Calcul du delta time
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - self.last_time) / 1000.0
            self.last_time = current_time
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return {"action": "quit"}
                
                result = self.menu.handle_event(event)
                if result == "start_game":
                    # Retourner l'action et les volumes
                    return {
                        "action": "start_game",
                        "music_volume": self.menu.music_volume,
                        "sfx_volume": self.menu.sfx_volume
                    }
                elif isinstance(result, dict) and result.get("action") == "start_game":
                    # Retourner le dictionnaire avec la map sélectionnée et les volumes
                    result["music_volume"] = self.menu.music_volume
                    result["sfx_volume"] = self.menu.sfx_volume
                    return result
                elif result == "quit":
                    return {"action": "quit"}
            
            self.menu.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return {"action": "quit"}


def main():
    """Fonction principale du menu"""
    try:
        menu_manager = MenuManager()
        result = menu_manager.run()
        
        pygame.quit()
        return result
        
    except Exception as e:
        print(f"Erreur dans le menu: {e}")
        traceback.print_exc()
        pygame.quit()
        return "quit"


if __name__ == "__main__":
    main()