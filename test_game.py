#!/usr/bin/env python3
"""
Test simple pour vérifier que le jeu fonctionne
"""

import os
import sys

# Ajouter le répertoire actuel au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pygame
    print("✓ Pygame importé avec succès")
    
    # Test d'initialisation
    pygame.init()
    print("✓ Pygame initialisé")
    
    # Test des modules du jeu
    from entities import Egg, Dinosaur, Trap
    print("✓ Module entities importé")
    
    from map_generator import MapGenerator
    print("✓ Module map_generator importé")
    
    from ui import UI
    print("✓ Module ui importé")
    
    from game import Game
    print("✓ Module game importé")
    
    # Test de création d'une instance de jeu (sans affichage)
    os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Mode sans affichage
    screen = pygame.display.set_mode((800, 600))
    game = Game(screen)
    print("✓ Instance de jeu créée")
    
    # Test des entités
    egg = Egg(1, 1, 1)
    print(f"✓ Œuf créé: joueur {egg.player}, position ({egg.x}, {egg.y}), vie {egg.health}")
    
    dino = Dinosaur(2, 2, 1, 1)
    print(f"✓ Dinosaure créé: type {dino.dino_type}, joueur {dino.player}, vie {dino.health}")
    
    trap = Trap(3, 3, 1)
    print(f"✓ Piège créé: joueur {trap.player}, position ({trap.x}, {trap.y})")
    
    # Test du générateur de carte
    map_gen = MapGenerator(10, 10)
    grid = map_gen.generate_map()
    print(f"✓ Carte générée: {len(grid)}x{len(grid[0])}")
    
    pygame.quit()
    print("\n🎉 Tous les tests sont passés! Le jeu devrait fonctionner correctement.")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)