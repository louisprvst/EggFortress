#!/usr/bin/env python3
"""
Test de la carte naturelle avec les nouveaux assets simples
"""

import pygame
import sys
import os

# Ajouter le dossier classes au path
sys.path.append('classes')
from map import Map

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Configuration de l'écran
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🌿 Egg Fortress - Carte Naturelle")
    
    # Créer la carte avec une taille de tuile adaptée
    tile_size = 64  # Taille des tuiles
    game_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT, tile_size)
    
    # Variables de caméra
    camera_x = 0
    camera_y = 0
    camera_speed = 8
    
    # Clock pour le FPS
    clock = pygame.time.Clock()
    
    print("🎮 Contrôles:")
    print("   WASD ou Flèches : Déplacer la caméra")
    print("   ESC ou Q : Quitter")
    print("   R : Régénérer la carte")
    print("   + / - : Changer la taille des tuiles")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    # Régénérer la carte
                    game_map.regenerate()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Augmenter la taille des tuiles
                    if tile_size < 128:
                        tile_size += 8
                        game_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT, tile_size)
                        print(f"📏 Taille des tuiles: {tile_size}px")
                elif event.key == pygame.K_MINUS:
                    # Diminuer la taille des tuiles
                    if tile_size > 32:
                        tile_size -= 8
                        game_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT, tile_size)
                        print(f"📏 Taille des tuiles: {tile_size}px")
        
        # Gestion des touches pour le mouvement de la caméra
        keys = pygame.key.get_pressed()
        
        # Mouvement de la caméra
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera_x = max(0, camera_x - camera_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            max_x = max(0, game_map.get_total_width() - SCREEN_WIDTH)
            camera_x = min(max_x, camera_x + camera_speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera_y = max(0, camera_y - camera_speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            max_y = max(0, game_map.get_total_height() - SCREEN_HEIGHT)
            camera_y = min(max_y, camera_y + camera_speed)
        
        # Remplir l'écran avec une couleur de fond naturelle
        screen.fill((135, 206, 235))  # Bleu ciel
        
        # Dessiner la carte
        game_map.draw(screen, camera_x, camera_y)
        
        # Afficher les informations de debug
        font = pygame.font.Font(None, 24)
        info_lines = [
            f"Caméra: ({camera_x}, {camera_y})",
            f"Carte: {game_map.get_total_width()}x{game_map.get_total_height()}px",
            f"Grille: {game_map.grid_width}x{game_map.grid_height}",
            f"Taille tuile: {tile_size}px",
            "R: Régénérer | +/-: Taille | WASD: Caméra"
        ]
        
        # Fond semi-transparent pour le texte
        info_height = len(info_lines) * 25 + 10
        pygame.draw.rect(screen, (0, 0, 0, 128), (5, 5, 350, info_height))
        
        # Afficher chaque ligne d'info
        for i, line in enumerate(info_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 25))
        
        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("👋 Au revoir!")

if __name__ == "__main__":
    main()