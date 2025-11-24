"""
Test de l'IA en mode headless (sans interface graphique)
Permet de tester rapidement le comportement de l'IA
"""

import sys
import os

# Simuler pygame pour le mode headless
class FakePygame:
    class time:
        @staticmethod
        def get_ticks():
            return 0
        @staticmethod
        def wait(ms):
            pass
    
    class display:
        @staticmethod
        def set_mode(size):
            return FakeSurface()
    
    class Surface:
        def __init__(self, size=(100, 100)):
            self.width, self.height = size
        
        def get_width(self):
            return self.width
        
        def get_height(self):
            return self.height
        
        def fill(self, color):
            pass
        
        def blit(self, surface, pos):
            pass
    
    QUIT = 0
    KEYDOWN = 1
    MOUSEBUTTONDOWN = 2
    K_SPACE = 32
    K_ESCAPE = 27
    K_r = 114

class FakeSurface(FakePygame.Surface):
    pass

# Remplacer pygame
sys.modules['pygame'] = FakePygame()
sys.modules['pygame.time'] = FakePygame.time
sys.modules['pygame.display'] = FakePygame.display

from game import Game
from ai.search_ai import SearchAI

def print_game_state(game):
    """Affiche l'état du jeu en mode texte"""
    print("\n" + "="*60)
    print(f"🎮 Tour {game.turn_number} - Joueur {'Bleu' if game.current_player == 1 else 'Rouge (IA)'}")
    print("="*60)
    
    # Ressources
    print(f"\n💰 Ressources:")
    print(f"   Joueur 1 (Bleu): {game.player1_steaks} steaks")
    print(f"   Joueur 2 (Rouge/IA): {game.player2_steaks} steaks")
    
    # Œufs
    print(f"\n🥚 Santé des œufs:")
    for player, egg in game.eggs.items():
        color = "Bleu" if player == 1 else "Rouge"
        print(f"   {color}: {egg.health}/{egg.max_health} HP (position: {egg.x}, {egg.y})")
    
    # Dinosaures
    print(f"\n🦖 Dinosaures:")
    dinos_p1 = [d for d in game.dinosaurs if d.player == 1]
    dinos_p2 = [d for d in game.dinosaurs if d.player == 2]
    
    print(f"   Joueur 1 (Bleu): {len(dinos_p1)} dinosaures")
    for i, d in enumerate(dinos_p1, 1):
        print(f"      {i}. Type {d.dino_type} - {d.health}/{d.max_health} HP - Pos({d.x},{d.y})")
    
    print(f"   Joueur 2 (Rouge/IA): {len(dinos_p2)} dinosaures")
    for i, d in enumerate(dinos_p2, 1):
        print(f"      {i}. Type {d.dino_type} - {d.health}/{d.max_health} HP - Pos({d.x},{d.y})")

def simulate_game(max_turns=10):
    """Simule une partie contre l'IA"""
    print("\n" + "🎮 " * 20)
    print("EGG FORTRESS - TEST IA EN MODE HEADLESS")
    print("🎮 " * 20)
    
    # Créer un faux écran
    screen = FakeSurface((1280, 720))
    game = Game(screen)
    
    print("\n✅ Jeu initialisé")
    print(f"   • IA activée pour le joueur {game.ai_player}")
    print(f"   • Algorithme: Minimax profondeur 2")
    print(f"   • Max réponses évaluées: {game.ai.max_enemy_responses}")
    
    turn = 0
    while turn < max_turns and not game.game_over:
        turn += 1
        print_game_state(game)
        
        if game.current_player == game.ai_player:
            print("\n🤖 L'IA réfléchit...")
            try:
                game.execute_ai_turn()
                print("   ✓ Action IA exécutée")
            except Exception as e:
                print(f"   ✗ Erreur IA: {e}")
                game.end_turn()
        else:
            print("\n👤 Tour du joueur humain (simulé)")
            # Simuler une action simple du joueur humain
            if game.player1_steaks >= 40:
                print("   • Spawn d'un dinosaure type 1")
                positions = game.calculate_spawn_positions()
                if positions:
                    x, y = positions[0]
                    game.spawn_dinosaur(x, y, 1)
            
            input("\n   Appuyez sur Entrée pour terminer le tour du joueur...")
            game.end_turn()
        
        # Petit délai pour lisibilité
        import time
        time.sleep(0.5)
    
    # Résultat final
    print("\n" + "🏆 " * 20)
    if game.game_over:
        winner = "Bleu (Joueur)" if game.winner == 1 else "Rouge (IA)"
        print(f"🎉 PARTIE TERMINÉE ! Vainqueur: {winner}")
    else:
        print(f"⏱️  LIMITE DE TOURS ATTEINTE ({max_turns} tours)")
    print("🏆 " * 20)
    
    print_game_state(game)
    
    print("\n📊 Statistiques finales:")
    print(f"   • Tours joués: {game.turn_number}")
    print(f"   • Dinosaures restants J1: {len([d for d in game.dinosaurs if d.player == 1])}")
    print(f"   • Dinosaures restants J2: {len([d for d in game.dinosaurs if d.player == 2])}")
    print(f"   • HP œuf J1: {game.eggs[1].health}")
    print(f"   • HP œuf J2: {game.eggs[2].health}")

if __name__ == "__main__":
    try:
        simulate_game(max_turns=20)
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
