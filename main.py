#!/usr/bin/env python3
import sys
import pygame
from game import Game
import traceback

def main():
    try: 
        # Créer et lancer le gestionnaire de menu
        menu_manager = MenuManager()
        
        # Lancer le menu
        result = menu_manager.run()
        
        if result and result == "start_game":
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            pygame.display.set_caption("Egg Fortress")
            
            clock = pygame.time.Clock()
            game = Game(screen)
            
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