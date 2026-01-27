#!/usr/bin/env python3
import sys
import os
import pygame
from game import Game
from menu import MenuManager
import traceback
from logger import get_logger, GameLogger

# Initialiser le logger
logger = get_logger("main")

def main():
    logger.info("Démarrage d'EggFortress")
    
    # Nettoyer les anciens logs (>30 jours) - échec silencieux
    try:
        GameLogger().cleanup_old_logs()
    except Exception as e:
        logger.warning(f"Impossible de nettoyer les anciens logs: {e}")
    
    try: 
        while True:  # Boucle pour permettre de revenir au menu
            # Créer et lancer le gestionnaire de menu
            menu_manager = MenuManager()
            
            # Lancer le menu
            result = menu_manager.run()
            
            if result:
                # Vérifier si c'est un dictionnaire (avec sélection de map) ou une chaîne
                if isinstance(result, dict) and result.get("action") == "start_game":
                    selected_map = result.get("map", "default")
                    game_mode = result.get("game_mode", "ai")
                    logger.info(f"Lancement du jeu - Map: {selected_map}, Mode: {game_mode}")
                    
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    pygame.display.set_caption("Egg Fortress")
                    
                    clock = pygame.time.Clock()
                    game = Game(screen, map_name=selected_map, game_mode=game_mode)
                    
                    # Appliquer les volumes du menu au jeu
                    game.set_volumes(result.get("music_volume", 0.3), result.get("sfx_volume", 1.0))
                    
                    # Boucle principale du jeu
                    running = True
                    while running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                pygame.quit()
                                return  # Quitter complètement
                            else:
                                game.handle_event(event)
                        
                        # Vérifier si on veut retourner au menu
                        if game.return_to_menu:
                            running = False
                            break  # Sortir de la boucle du jeu pour retourner au menu
                        
                        # Vérifier si la surface est toujours valide avant de dessiner
                        if not pygame.display.get_surface():
                            running = False
                            break
                            
                        game.update()
                        game.draw()
                        pygame.display.flip()
                        clock.tick(60)
                else:
                    # Si on quitte le menu sans jouer
                    logger.info("Retour au menu sans lancer de partie")
                    break
            else:
                # Si le menu retourne None (fermeture)
                logger.info("Fermeture du menu")
                break
        
        logger.info("Fermeture normale d'EggFortress")
        pygame.quit()
        
    except Exception as e:
        logger.critical(f"Erreur critique lors de l'exécution: {e}")
        logger.critical("Détails de l'erreur:")
        logger.critical(traceback.format_exc())
        
        try:
            pygame.quit()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()