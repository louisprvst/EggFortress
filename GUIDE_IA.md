# 🤖 Guide d'utilisation de l'IA - Egg Fortress

## 🚀 Démarrage rapide

### Jouer contre l'IA
```bash
python main.py
```
- Cliquez sur **JOUER** dans le menu
- Vous êtes le joueur **BLEU**
- L'IA joue automatiquement en **ROUGE** après votre tour

### Script de test avec logs
```bash
python play_vs_ai.py
```
Affiche des informations détaillées sur l'IA dans la console.

### Test en mode headless (sans interface)
```bash
python test_ai_headless.py
```
Simule une partie complète en mode console pour tester l'IA.

## 🎮 Comment jouer contre l'IA

### Votre tour (Joueur Bleu)
1. **Spawner** des dinosaures en cliquant sur les boutons en bas
2. **Déplacer** vos dinosaures en les sélectionnant puis en cliquant sur une case
3. **Attaquer** en cliquant sur le bouton rouge "ATTAQUE" puis sur la cible
4. Appuyez sur **ESPACE** pour terminer votre tour

### Tour de l'IA (Joueur Rouge)
- L'IA réfléchit pendant ~1 seconde
- Elle exécute automatiquement ses actions
- Vous pouvez voir ses décisions dans la console si `verbose=True`

## 🧠 Comprendre l'IA

### Ce que l'IA fait bien
✅ Protège son œuf efficacement
✅ Attaque de manière stratégique
✅ Gère ses ressources intelligemment
✅ Anticipe vos réponses

### Limites de l'IA
❌ Profondeur limitée (2 coups à l'avance)
❌ Peut être prévisible
❌ Ne voit pas les stratégies à très long terme

## ⚙️ Personnalisation

### Changer la difficulté

Éditez `game.py`, ligne ~127 :

```python
# Facile (rapide, moins forte)
self.ai = SearchAI(player=2, max_enemy_responses=5, verbose=True)

# Normal (défaut)
self.ai = SearchAI(player=2, max_enemy_responses=8, verbose=True)

# Difficile (lent, très forte)
self.ai = SearchAI(player=2, max_enemy_responses=15, verbose=True)
```

### Désactiver les logs de l'IA

```python
self.ai = SearchAI(player=2, max_enemy_responses=8, verbose=False)
```

### Changer le joueur IA

Pour que l'IA joue en BLEU (joueur 1) :

```python
self.ai_player = 1  # Au lieu de 2
self.ai = SearchAI(player=1, max_enemy_responses=8, verbose=True)
```

### Ajuster le délai de l'IA

Dans `game.py`, ligne ~129 :

```python
self.ai_action_delay = 0.5  # Plus rapide
# ou
self.ai_action_delay = 2.0  # Plus lent (pour mieux voir)
```

## 📊 Statistiques de l'IA

### Performance moyenne
- **Temps de décision** : 0.5-2 secondes/tour
- **Actions évaluées** : 30-50 par tour
- **Simulations** : ~240 états (30 actions × 8 réponses)

### Comportement observé
- **Ouverture** : Spawn de dinosaures équilibrés ou tanks
- **Milieu de partie** : Pression offensive + défense
- **Fin de partie** : Attaques directes sur l'œuf

## 🐛 Dépannage

### L'IA ne joue pas
Vérifiez dans la console :
- Y a-t-il des erreurs ?
- Les logs "=== IA Joueur 2 réfléchit ===" apparaissent-ils ?

### L'IA joue trop lentement
Réduisez `max_enemy_responses` :
```python
self.ai = SearchAI(player=2, max_enemy_responses=5)
```

### L'IA fait des actions invalides
C'est un bug ! Vérifiez :
1. Les logs d'erreur dans la console
2. Le fichier `ai/game_simulator.py` (simulation d'état)
3. Ouvrez une issue sur GitHub

## 🔧 Développement

### Créer une nouvelle IA

1. Créez un fichier dans `ai/` (ex: `my_ai.py`)
2. Héritez de `BaseAI` :

```python
from ai.base_ai import BaseAI
import random

class MyAI(BaseAI):
    def choose_action(self, game):
        # Votre logique ici
        actions = self.generate_actions(game, self.player)
        return random.choice(actions)
```

3. Utilisez-la dans `game.py` :

```python
from ai.my_ai import MyAI

# Dans Game.__init__()
self.ai = MyAI(player=2)
```

### Tester votre IA

```bash
# Mode graphique
python main.py

# Mode console
python test_ai_headless.py
```

## 📚 Ressources

- **Documentation IA complète** : `ai/README.md`
- **Code source IA** : Dossier `ai/`
- **Algorithme Minimax** : https://en.wikipedia.org/wiki/Minimax
- **Heuristiques de jeu** : `ai/heuristics.py`

## 🎯 Conseils pour battre l'IA

1. **Variez vos stratégies** : L'IA s'adapte mais peut être surprise
2. **Protégez votre œuf** : L'IA est agressive
3. **Utilisez les tanks** : Efficaces pour défendre
4. **Attaques coordonnées** : Plusieurs dinosaures en même temps
5. **Gestion des ressources** : Ne dépensez pas tout d'un coup

Bonne chance ! 🎮
