import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys

from menu import Menu
from game_map import GameMap

def main():
    pygame.init()
    ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Egg Fortress")
    
    running = True
    while running:
        # Lancer le menu
        menu = Menu(ecran)
        resultat = menu.executer()
        
        if resultat == "jouer":
            # Lancer la map interactive
            game_map = GameMap(ecran)
            resultat_map = game_map.executer()
            
            if resultat_map == "quitter":
                running = False
            # Si resultat_map == "menu", on retourne au menu
        else:
            running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()