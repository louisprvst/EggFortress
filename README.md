# Egg Fortress

Un jeu de stratégie au tour par tour créé avec Pygame où deux joueurs s'affrontent pour protéger leur œuf et détruire celui de l'adversaire.

## 🎮 Menu Principal

**Egg Fortress** dispose d'un **menu d'accueil complet** avec :
- **Page d'accueil animée** avec dinosaures flottants
- **Bouton JOUER** pour lancer le jeu en mode 2 joueurs
- **Menu PARAMÈTRES** avec guide complet "Comment Jouer"
- **Interface intuitive** et design attractif

## Fonctionnalités

- **Système de tour par tour** : Chaque joueur joue à son tour
- **Trois types de dinosaures** :
  - Type 1 (40 steaks) : Rapide, faible en vie, attaque moyenne
  - Type 2 (80 steaks) : Équilibré en vitesse, vie et attaque
  - Type 3 (100 steaks) : Lent, forte vie, attaque puissante
- **Système de ressources** : Gagnez 20 steaks par tour et des bonus en tuant des ennemis
- **Pièges** : Placez des pièges pour endommager les dinosaures ennemis
- **Cartes aléatoires** : Chaque partie génère une nouvelle carte
- **Barres de vie** : Suivez la santé de vos œufs et dinosaures

## Installation

1. Assurez-vous d'avoir Python 3.7+ installé
2. Clonez ou téléchargez le projet
3. Naviguez dans le dossier du projet
4. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Lancement du jeu

```bash
python main.py
```

Le jeu se lance avec un menu principal. Cliquez sur **JOUER** pour commencer une partie en mode 2 joueurs.

## Contrôles

- **Clic gauche** : Sélectionner un dinosaure ou une destination/cible
- **Boutons UI** : Spawner des dinosaures ou placer des pièges
- **ESPACE** : Terminer votre tour
- **ÉCHAP** : Annuler l'action en cours
- **R** : Redémarrer (en fin de partie)

### Combat
- **Cases bleues** : Mouvements possibles pour le dinosaure sélectionné
- **Bouton rouge "ATTAQUE"** : Apparaît quand des ennemis sont adjacents
- **Clic sur bouton → Mode attaque** : Cases rouges sur les cibles
- **Clic sur cible rouge** : Attaquer immédiatement

## Règles du jeu

1. Chaque joueur commence avec 100 steaks
2. Gagnez 20 steaks à chaque tour
3. Spawner des dinosaures près de votre œuf (distance max: 3 cases)
4. Déplacez vos dinosaures pour attaquer l'ennemi
5. **Attaquez** les dinosaures ennemis ou leur œuf directement
6. Protégez votre œuf - s'il meurt, vous perdez !
7. Les pièges infligent 50 dégâts et immobilisent pendant 2 tours
8. **Combat avec riposte** : L'ennemi riposte à 50% des dégâts
9. **+20 steaks** pour chaque dinosaure ennemi éliminé

## Types de dinosaures

### Type 1 - Rapide (40 steaks)
- Vie: 60
- Attaque: 30
- Mouvement: 3 cases
- **Stratégie**: Harcèlement et mobilité

### Type 2 - Équilibré (80 steaks)
- Vie: 80
- Attaque: 45
- Mouvement: 2 cases
- **Stratégie**: Polyvalent, contrôle de zone

### Type 3 - Tank (100 steaks)
- Vie: 120
- Attaque: 60
- Mouvement: 1 case
- **Stratégie**: Défense d'œuf et attaque lourde

## Structure du projet

- `launcher.py` : Lanceur principal avec options
- `main.py` : Point d'entrée original du jeu
- `simple_main.py` : Version simplifiée pour test
- `console_game.py` : Version console du jeu
- `game.py` : Logique principale du jeu
- `entities.py` : Classes pour les œufs, dinosaures et pièges
- `map_generator.py` : Génération de cartes aléatoires
- `ui.py` : Interface utilisateur
- `assets/` : Images et sons du jeu
- `test_game.py` : Tests des modules

## Dépannage

Si le jeu ne se lance pas :
1. Vérifiez que pygame est installé : `pip install pygame`
2. Testez les modules : `python test_game.py`
3. Essayez le mode console : `python launcher.py --console`
4. Utilisez le mode headless pour tester la logique : `python launcher.py --headless`