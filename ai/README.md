# IA pour Egg Fortress

## 📋 Vue d'ensemble

Ce dossier contient l'implémentation d'une **IA avec recherche à profondeur 2** (Minimax simplifié) pour le jeu Egg Fortress. L'IA joue automatiquement pour le **joueur rouge (joueur 2)** après que le joueur bleu (joueur humain) ait terminé son tour.

## 🧠 Algorithme

L'IA utilise une approche **Minimax simplifiée** avec les caractéristiques suivantes :

### Profondeur de recherche : 2
1. **Niveau 1** : L'IA simule toutes ses actions possibles
2. **Niveau 2** : Pour chaque action, elle anticipe les meilleures réponses de l'adversaire
3. **Décision** : Elle choisit l'action qui maximise son avantage après la riposte ennemie

### Fonction d'évaluation heuristique

L'IA évalue chaque état de jeu selon plusieurs critères pondérés :

- **Santé des œufs** (×10) : Priorité maximale
- **Nombre de dinosaures** (×50) : Contrôle du plateau
- **Santé totale des dinosaures** (×2) : Force de l'armée
- **Ressources (steaks)** (×0.5) : Capacité future
- **Proximité à l'œuf ennemi** (×3) : Pression offensive
- **Distance des ennemis à mon œuf** (×2) : Défense
- **Bonus pour tanks proches de l'objectif** (+30) : Stratégie spécifique

### Optimisations

- **Échantillonnage** : Limite à 8 les meilleures réponses ennemies évaluées par action
- **Bruit aléatoire** : Petite variation pour éviter les comportements déterministes
- **Simulation légère** : Copie d'état sans objets pygame pour la performance

## 📁 Structure des fichiers

```
ai/
├── __init__.py           # Point d'entrée du module
├── base_ai.py            # Classe abstraite pour toutes les IA
├── search_ai.py          # Implémentation de l'IA Minimax
├── game_simulator.py     # Copie et simulation d'états de jeu
├── heuristics.py         # Fonctions d'évaluation
└── README.md             # Ce fichier
```

## 🎯 Utilisation

L'IA est automatiquement activée dans `game.py` :

```python
# Dans Game.__init__()
self.ai_player = 2  # Joueur rouge
self.ai = SearchAI(player=2, max_enemy_responses=8, verbose=True)
```

### Paramètres configurables

- `player` : Numéro du joueur IA (1 ou 2)
- `max_enemy_responses` : Nombre max de réponses adverses à évaluer (défaut: 8)
- `verbose` : Afficher les logs de décision dans la console (défaut: True)

### Modifier la difficulté

Pour ajuster la force de l'IA, modifiez dans `game.py` :

```python
# IA plus rapide mais moins forte
self.ai = SearchAI(player=2, max_enemy_responses=5, verbose=False)

# IA plus lente mais plus forte
self.ai = SearchAI(player=2, max_enemy_responses=12, verbose=False)
```

## 🔧 Fonctionnement technique

### 1. Détection du tour IA

Dans `game.py`, la méthode `update()` détecte quand c'est le tour de l'IA :

```python
if not self.game_over and self.current_player == self.ai_player:
    if not self.ai_thinking and not self.spawn_action_done:
        self.ai_action_timer += delta_time
        if self.ai_action_timer >= self.ai_action_delay:
            self.execute_ai_turn()
```

### 2. Choix d'action

L'IA génère toutes les actions légales :
- **Spawn** : Créer un dinosaure (type 1/2/3)
- **Move** : Déplacer un dinosaure
- **Attack** : Attaquer un dinosaure ou un œuf ennemi
- **Trap** : Placer un piège
- **Pass** : Passer le tour

### 3. Simulation et évaluation

Pour chaque action, l'IA :
1. Copie l'état du jeu
2. Simule l'action
3. Génère les réponses ennemies
4. Évalue l'état résultant
5. Choisit l'action avec le meilleur score minimum (principe minimax)

### 4. Exécution

L'action choisie est exécutée via `execute_ai_action()` avec :
- Délais visuels pour voir les actions
- Support multi-actions par tour (mouvements/attaques multiples)
- Fin automatique après spawn ou piège

## 📊 Performance

- **Temps de décision moyen** : 0.5-2 secondes par tour
- **Actions évaluées** : ~30-50 par tour
- **Simulations par tour** : ~240 (30 actions × 8 réponses)

## 🎮 Comportement de l'IA

### Stratégie offensive
- Spawn de dinosaures près de son œuf
- Déplacement vers l'œuf ennemi
- Attaque prioritaire des dinosaures faibles ou de l'œuf

### Stratégie défensive
- Protection de son propre œuf
- Élimination des menaces proches
- Gestion des ressources pour spawns futurs

### Points forts
- Anticipe les ripostes adverses
- Prend des décisions cohérentes
- Protège son œuf efficacement
- Optimise attaques/déplacements

### Points faibles
- Profondeur limitée (pas de stratégie long terme)
- Peut être prévisible avec le temps
- Ne gère pas les situations très complexes

## 🔄 Évolutions futures possibles

1. **Augmenter la profondeur** : Passer à profondeur 3 ou 4 avec alpha-beta pruning
2. **Apprentissage** : Intégrer Q-learning pour améliorer les heuristiques
3. **Monte-Carlo** : Utiliser MCTS pour des décisions plus robustes
4. **Réglages adaptatifs** : Ajuster la difficulté selon le niveau du joueur
5. **Stratégies variées** : Ajouter des "personnalités" (agressif, défensif, équilibré)

## 🐛 Debug

Pour activer les logs détaillés :

```python
self.ai = SearchAI(player=2, max_enemy_responses=8, verbose=True)
```

Les logs affichent :
- Nombre d'actions possibles
- Type d'action choisie
- Score de l'action

Exemple :
```
=== IA Joueur 2 réfléchit ===
48 actions possibles
Meilleure action: spawn (score: 213.1)
```

## 📝 Notes de développement

- L'IA utilise une copie légère de l'état sans objets pygame pour éviter les erreurs de sérialisation
- Les délais entre actions permettent au joueur de voir les mouvements de l'IA
- Le système supporte plusieurs actions par tour (mouvements multiples) sauf après spawn/piège
- Les dinosaures déjà déplacés sont exclus des actions possibles

## 🤝 Contribution

Pour ajouter une nouvelle IA :

1. Créer une nouvelle classe héritant de `BaseAI`
2. Implémenter la méthode `choose_action(game)`
3. Instancier dans `game.py` : `self.ai = YourAI(player=2)`

Exemple :

```python
from ai.base_ai import BaseAI

class RandomAI(BaseAI):
    def choose_action(self, game):
        import random
        actions = self.generate_actions(game)
        return random.choice(actions)
```
