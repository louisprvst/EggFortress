import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys

from menu import Menu

def main():
    pygame.init()
    ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Egg Fortress")
    
    # Lancer le menu
    menu = Menu(ecran)
    resultat = menu.executer()
    
    if resultat == "jouer":
        # TODO: Lancer le jeu ici
        print("Lancement du jeu...")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()