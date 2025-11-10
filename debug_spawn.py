#!/usr/bin/env python3
import os
import sys
import pygame
from game import Game

# S'assurer que pygame fonctionne en mode dummy si pas d'affichage
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

pygame.init()
screen = pygame.display.set_mode((800, 600))

g = Game(screen)

# Afficher position de l'oeuf principal du joueur 1
egg = g.eggs[1]
print('Main egg pos:', egg.x, egg.y)

# Trouver une case de spawn valide
spawn_positions = g.calculate_spawn_positions()
print('Possible spawn positions sample:', spawn_positions[:5])

if not spawn_positions:
    print('No spawn positions available, abort')
    sys.exit(1)

x, y = spawn_positions[0]
print('Spawning at', x, y)
# Spawn d'un type 1
g.spawn_dinosaur(x, y, 1)

print('Spawn eggs count:', len(g.spawn_eggs))
se = g.spawn_eggs[0]
print('Initial spawn_turns_required:', se.spawn_turns_required)
print('Initial spawn_turns_elapsed:', se.spawn_turns_elapsed)
print('Initial spawn_progress:', se.spawn_progress)

# Appeler end_turn plusieurs fois et afficher l'état
for t in range(1, 6):
    print('\n--- End turn', t, '---')
    g.end_turn()
    # état de l'oeuf
    if g.spawn_eggs:
        se = g.spawn_eggs[0]
        remaining = se.spawn_turns_required - se.spawn_turns_elapsed
        print('spawn_turns_elapsed:', se.spawn_turns_elapsed)
        print('remaining:', remaining)
        print('is_hatching:', se.is_hatching)
        print('is_ready_to_hatch:', se.is_ready_to_hatch())
    else:
        print('No spawn_eggs remain (hatched)')
        break

pygame.quit()
print('\nDebug done')