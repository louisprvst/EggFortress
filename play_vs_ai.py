"""
Script de test pour l'IA de Egg Fortress
Lance le jeu en mode Joueur vs IA
"""

import pygame
from game import Game
from menu import Menu

def main():
    """Lance le jeu avec l'IA activée"""
    pygame.init()
    
    # Configuration de la fenêtre
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Egg Fortress - Joueur vs IA")
    
    # Charger le menu
    menu = Menu(screen)
    clock = pygame.time.Clock()
    
    print("=" * 60)
    print("🎮 EGG FORTRESS - MODE JOUEUR VS IA")
    print("=" * 60)
    print("\n📋 Instructions:")
    print("  • Le joueur BLEU (vous) joue en premier")
    print("  • Le joueur ROUGE (IA) joue automatiquement après vous")
    print("  • Cliquez sur JOUER dans le menu pour commencer")
    print("\n🎯 Objectif:")
    print("  • Détruisez l'œuf ennemi avant que l'IA détruise le vôtre")
    print("\n⚙️  Configuration IA:")
    print("  • Algorithme: Minimax profondeur 2")
    print("  • Difficulté: Intermédiaire")
    print("  • Actions évaluées: ~8 réponses ennemies par action")
    print("\n💡 Conseils:")
    print("  • L'IA anticipe vos réponses, soyez stratégique")
    print("  • Protégez votre œuf tout en attaquant")
    print("  • Utilisez différents types de dinosaures")
    print("\n" + "=" * 60)
    print("Appuyez sur ESPACE pour passer votre tour")
    print("Appuyez sur ÉCHAP pour annuler une action")
    print("=" * 60 + "\n")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            menu.handle_event(event)
        
        menu.update()
        menu.draw()
        pygame.display.flip()
        clock.tick(60)
        
        # Vérifier si le jeu a démarré
        if menu.game_started and menu.game:
            # Le jeu est en cours
            break
    
    # Boucle de jeu principale
    if menu.game_started and menu.game:
        game = menu.game
        
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
            
            # Retour au menu si le jeu est terminé et qu'on appuie sur R
            if game.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        game.restart_game()
    
    pygame.quit()
    print("\n👋 Merci d'avoir joué à Egg Fortress!")

if __name__ == "__main__":
    main()
