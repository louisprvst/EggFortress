#!/usr/bin/env python3
import sys
import os

def main():
    try:
        # Essayer d'importer pygame
        import pygame
        print("✓ Pygame trouvé et importé avec succès")
    except ImportError:
        print("❌ ERREUR: pygame n'est pas installé ou accessible")
        print()
        print("🔧 SOLUTIONS:")
        print("1. Utiliser l'environnement virtuel:")
        print("   /Users/nadirelmoutaouakil/Documents/egg/.venv/bin/python main.py")
        print()
        print("2. Ou installer pygame globalement:")
        print("   pip install pygame")
        print()
        print("3. Ou essayer la version console:")
        print("   /Users/nadirelmoutaouakil/Documents/egg/.venv/bin/python launcher.py --console")
        print()
        sys.exit(1)
    
    try:
        # Lancer le menu principal
        from menu import MenuManager
        print("✓ Module de menu importé")
        
        # Créer et lancer le gestionnaire de menu
        menu_manager = MenuManager()
        print("✓ EGG FORTRESS - Menu principal lancé!")
        print()
        print("🎮 BIENVENUE DANS EGG FORTRESS!")
        print("- Utilisez le menu pour naviguer")
        print("- Cliquez sur JOUER pour commencer")
        print("- Consultez PARAMÈTRES pour les règles")
        print()
        
        # Lancer le menu
        result = menu_manager.run()
        
        if result and result == "start_game":
            # Lancer le jeu principal
            print("🎮 EGG FORTRESS")
            print("Lancement du jeu en mode 2 joueurs...")
            
            from game import Game
            screen = pygame.display.set_mode((1200, 800))
            pygame.display.set_caption("Egg Fortress")
            
            clock = pygame.time.Clock()
            game = Game(screen)
            
            print("✓ Mode 2 joueurs activé")
            print("✓ Jeu initialisé depuis le menu!")
            print()
            print("🎮 CONTRÔLES:")
            print("- Clic gauche: Sélectionner/Déplacer")
            print("- Boutons: Spawner dinosaures/pièges")
            print("- ESPACE: Finir le tour")
            print("- ÉCHAP: Annuler action")
            print("- R: Redémarrer (fin de partie)")
            print()
            print("🎯 OBJECTIF: Détruisez l'œuf ennemi!")
            
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
        print("✓ Jeu fermé normalement")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        print()
        print("🔧 Suggestions:")
        print("1. Vérifiez que tous les fichiers sont présents")
        print("2. Essayez: python test_game.py")
        print("3. Utilisez le mode console: python launcher.py --console")
        
        import traceback
        print("\n📋 Détails de l'erreur:")
        traceback.print_exc()
        
        try:
            pygame.quit()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()