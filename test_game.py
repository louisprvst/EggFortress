#!/usr/bin/env python3
"""
Test simple pour vérifier que le jeu fonctionne
"""

import os
import sys
import pygame
from entities import Egg, Dinosaur, Trap
from map_generator import MapGenerator
from map_generator import MapGenerator
from game import Game
import traceback

# Ajouter le répertoire actuel au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    pygame.init()
    
    # Test de création d'une instance de jeu (sans affichage)
    os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Mode sans affichage
    screen = pygame.display.set_mode((800, 600))
    game = Game(screen)
    
    # Test des entités
    egg = Egg(1, 1, 1)
    
    dino = Dinosaur(2, 2, 1, 1)
    
    trap = Trap(3, 3, 1)
    
    # Test du générateur de carte
    map_gen = MapGenerator(10, 10)
    grid = map_gen.generate_map()
    
    pygame.quit()
    
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Erreur: {e}")
    traceback.print_exc()
    sys.exit(1)