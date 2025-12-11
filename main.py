#!/usr/bin/env python3
import sys
import os
import pygame
from game import Game
from menu import MenuManager
import traceback

def main():
    try: 
        # Créer et lancer le gestionnaire de menu
        menu_manager = MenuManager()
        
        # Lancer le menu
        result = menu_manager.run()
        
        if result:
            # Vérifier si c'est un dictionnaire (avec sélection de map) ou une chaîne
            if isinstance(result, dict) and result.get("action") == "start_game":
                selected_map = result.get("map", "default")
                screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                pygame.display.set_caption("Egg Fortress")
                
                clock = pygame.time.Clock()
                game = Game(screen, map_name=selected_map)
                
                # Appliquer les volumes du menu au jeu
                game.set_volumes(result.get("music_volume", 0.3), result.get("sfx_volume", 1.0))
                
                # Boucle principale du jeu
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        else:
                            game.handle_event(event)
                    
                    game.update()
                    game.draw()
                    pygame.display.flip()
                    clock.tick(60)
        
        pygame.quit()
        
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        
        print("\nDétails de l'erreur:")
        traceback.print_exc()
        
        try:
            pygame.quit()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()