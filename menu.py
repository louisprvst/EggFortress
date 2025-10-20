#!/usr/bin/env python3
"""
Menu principal pour Egg Fortress
"""

import pygame
import sys
import os
import math
import random

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Polices
        self.title_font = pygame.font.Font(None, 96)
        self.button_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        
        # États du menu
        self.current_screen = "main"  # "main", "settings", "how_to_play"
        
        # Animation
        self.time = 0
        self.dino_positions = []
        self.init_dino_animations()
        
        # Boutons
        self.buttons = {
            "play": pygame.Rect(self.screen_width//2 - 150, 400, 300, 80),
            "settings": pygame.Rect(self.screen_width//2 - 150, 500, 300, 80),
            "quit": pygame.Rect(self.screen_width//2 - 150, 600, 300, 80),
            "back": pygame.Rect(50, self.screen_height - 100, 150, 60)
        }
        
        # Charger les images des dinosaures si disponibles
        self.dino_images = self.load_dino_images()
        
    def load_dino_images(self):
        """Charge les images des dinosaures pour l'animation"""
        images = {}
        try:
            # Charger les images de dinosaures des assets
            for i in range(1, 4):  # Types 1, 2, 3
                for color in ["Blue", "Red"]:
                    img_path = f"assets/images/Dinos/Dino{i}_{color}.png"
                    if os.path.exists(img_path):
                        img = pygame.image.load(img_path)
                        # Redimensionner pour le menu
                        img = pygame.transform.scale(img, (80, 80))
                        images[f"dino{i}_{color.lower()}"] = img
        except:
            pass
        return images
    
    def init_dino_animations(self):
        """Initialise les positions d'animation des dinosaures"""
        for i in range(6):  # 6 dinosaures animés
            self.dino_positions.append({
                'x': random.randint(50, self.screen_width - 100),
                'y': random.randint(200, self.screen_height - 200),
                'speed': random.uniform(0.5, 2.0),
                'direction': random.uniform(0, 2 * math.pi),
                'type': random.randint(1, 3),
                'color': random.choice(['blue', 'red']),
                'bounce_time': random.uniform(0, 10)
            })
    
    def update(self, delta_time):
        """Met à jour les animations"""
        self.time += delta_time
        
        # Animer les dinosaures
        for dino in self.dino_positions:
            dino['bounce_time'] += delta_time
            
            # Mouvement flottant
            dino['x'] += math.cos(dino['direction']) * dino['speed']
            dino['y'] += math.sin(dino['direction']) * dino['speed']
            
            # Rebond sur les bords
            if dino['x'] <= 50 or dino['x'] >= self.screen_width - 100:
                dino['direction'] = math.pi - dino['direction']
            if dino['y'] <= 150 or dino['y'] >= self.screen_height - 150:
                dino['direction'] = -dino['direction']
            
            # Garder dans les limites
            dino['x'] = max(50, min(self.screen_width - 100, dino['x']))
            dino['y'] = max(150, min(self.screen_height - 150, dino['y']))
    
    def handle_event(self, event):
        """Gère les événements du menu"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.current_screen == "main":
                if self.buttons["play"].collidepoint(mouse_pos):
                    return "start_game"
                elif self.buttons["settings"].collidepoint(mouse_pos):
                    self.current_screen = "settings"
                elif self.buttons["quit"].collidepoint(mouse_pos):
                    return "quit"
            
            elif self.current_screen in ["settings", "how_to_play"]:
                if self.buttons["back"].collidepoint(mouse_pos):
                    self.current_screen = "main"
            
            # Bouton "Comment jouer" dans les paramètres
            if self.current_screen == "settings":
                how_to_play_button = pygame.Rect(self.screen_width//2 - 200, 300, 400, 80)
                if how_to_play_button.collidepoint(mouse_pos):
                    self.current_screen = "how_to_play"
        
        return None
    
    def draw(self):
        """Dessine le menu"""
        if self.current_screen == "main":
            self.draw_main_menu()
        elif self.current_screen == "settings":
            self.draw_settings()
        elif self.current_screen == "how_to_play":
            self.draw_how_to_play()
    
    def draw_main_menu(self):
        """Dessine le menu principal"""
        # Fond dégradé
        self.draw_gradient_background()
        
        # Dinosaures animés en arrière-plan
        self.draw_animated_dinos()
        
        # Titre principal
        title_text = self.title_font.render("EGG FORTRESS", True, (255, 255, 255))
        title_shadow = self.title_font.render("EGG FORTRESS", True, (0, 0, 0))
        
        title_rect = title_text.get_rect(center=(self.screen_width//2, 150))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle = self.text_font.render("Défendez votre œuf ! Détruisez celui de l'ennemi !", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen_width//2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Boutons
        self.draw_button("play", "JOUER", (0, 200, 0), (0, 255, 0))
        self.draw_button("settings", "PARAMÈTRES", (100, 100, 200), (150, 150, 255))
        self.draw_button("quit", "QUITTER", (200, 100, 100), (255, 150, 150))
    
    def draw_game_mode_selection(self):
        """Dessine l'écran de sélection du mode de jeu"""
        # Fond dégradé
        self.draw_gradient_background()
        
        # Dinosaures animés en arrière-plan (plus faibles)
        self.draw_animated_dinos()
        
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
        subtitle = self.text_font.render("Choisissez votre adversaire :", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.screen_width//2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Description du mode sélectionné
        if self.selected_game_mode == "ai":
            desc_text = "Affrontez une Intelligence Artificielle stratégique"
            desc_color = (150, 255, 150)
        else:
            desc_text = "Jouez contre un autre joueur sur le même ordinateur"
            desc_color = (255, 150, 150)
        
        description = self.text_font.render(desc_text, True, desc_color)
        desc_rect = description.get_rect(center=(self.screen_width//2, 220))
        self.screen.blit(description, desc_rect)
        
        # Boutons de sélection avec icônes
        # Bouton IA
        ai_selected = self.selected_game_mode == "ai"
        ai_color = (0, 255, 0) if ai_selected else (100, 200, 100)
        ai_hover_color = (50, 255, 50) if ai_selected else (150, 255, 150)
        
        self.draw_game_mode_button("vs_ai", "🤖 VS IA", ai_color, ai_hover_color, ai_selected)
        
        # Bouton Joueur
        human_selected = self.selected_game_mode == "human"
        human_color = (255, 100, 100) if human_selected else (200, 100, 100)
        human_hover_color = (255, 150, 150) if human_selected else (255, 150, 150)
        
        self.draw_game_mode_button("vs_human", "👥 VS JOUEUR", human_color, human_hover_color, human_selected)
        
        # Bouton Commencer avec le mode sélectionné
        start_text = f"COMMENCER ({self.selected_game_mode.upper()})"
        self.draw_button("start_selected", start_text, (255, 165, 0), (255, 200, 50))
        
        # Bouton retour
        self.draw_button("back", "RETOUR", (100, 100, 100), (150, 150, 150))
    
    def draw_settings(self):
        """Dessine le menu des paramètres"""
        self.draw_gradient_background()
        
        # Titre
        title = self.title_font.render("PARAMÈTRES", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width//2, 100))
        self.screen.blit(title, title_rect)
        
        # Bouton Comment jouer
        how_to_play_button = pygame.Rect(self.screen_width//2 - 200, 300, 400, 80)
        self.draw_custom_button(how_to_play_button, "COMMENT JOUER", (100, 150, 200), (150, 200, 255))
        
        # Informations du jeu
        info_texts = [
            "Version: 1.0",
            "Créé avec Pygame",
            "Jeu de stratégie au tour par tour"
        ]
        
        y_start = 450
        for i, text in enumerate(info_texts):
            info_surface = self.text_font.render(text, True, (200, 200, 200))
            info_rect = info_surface.get_rect(center=(self.screen_width//2, y_start + i * 40))
            self.screen.blit(info_surface, info_rect)
        
        # Bouton retour
        self.draw_button("back", "RETOUR", (150, 150, 150), (200, 200, 200))
    
    def draw_how_to_play(self):
        """Dessine l'écran des règles"""
        self.draw_gradient_background()
        
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
    
    def draw_gradient_background(self):
        """Dessine un fond dégradé"""
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            # Dégradé du bleu foncé au noir
            r = int(20 * (1 - ratio))
            g = int(30 * (1 - ratio))
            b = int(60 * (1 - ratio))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen_width, y))
    
    def draw_animated_dinos(self):
        """Dessine les dinosaures animés en arrière-plan"""
        for dino in self.dino_positions:
            # Effet de flottement
            float_offset = math.sin(dino['bounce_time'] * 2) * 5
            
            x = int(dino['x'])
            y = int(dino['y'] + float_offset)
            
            # Utiliser l'image si disponible, sinon dessiner un cercle
            key = f"dino{dino['type']}_{dino['color']}"
            if key in self.dino_images:
                # Effet de transparence
                img = self.dino_images[key].copy()
                img.set_alpha(100)  # Semi-transparent
                img_rect = img.get_rect(center=(x, y))
                self.screen.blit(img, img_rect)
            else:
                # Fallback: dessiner un cercle coloré
                color = (100, 100, 255) if dino['color'] == 'blue' else (255, 100, 100)
                pygame.draw.circle(self.screen, color, (x, y), 30, 3)
                # Petit cercle au centre
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 5)
    
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
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
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
                    return "quit"
                
                result = self.menu.handle_event(event)
                if result == "start_game":
                    return "start_game"
                elif result == "quit":
                    return "quit"
            
            # Mise à jour et rendu
            self.menu.update(delta_time)
            self.menu.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return "quit"


def main():
    """Fonction principale du menu"""
    try:
        menu_manager = MenuManager()
        result = menu_manager.run()
        
        pygame.quit()
        return result
        
    except Exception as e:
        print(f"Erreur dans le menu: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return "quit"


if __name__ == "__main__":
    main()