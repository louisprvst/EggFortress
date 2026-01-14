"""
IA avec recherche à profondeur 2 (Minimax simplifié)
Anticipe les réponses de l'adversaire pour prendre des décisions robustes
"""

from ai.base_ai import BaseAI
from ai.game_simulator import GameSimulator
from ai.heuristics import evaluate_state
import random

class SearchAI(BaseAI):
    """IA avec recherche à profondeur 2 (Minimax simplifié)"""
    
    def __init__(self, player, max_enemy_responses=8, verbose=False):
        """
        Initialise l'IA de recherche
        
        Args:
            player (int): Numéro du joueur (1 ou 2)
            max_enemy_responses (int): Nombre max de réponses ennemies à évaluer
            verbose (bool): Afficher les logs de décision
        """
        super().__init__(player)
        self.max_enemy_responses = max_enemy_responses
        self.verbose = verbose
    
    def choose_action(self, game):
        """
        Choisit la meilleure action en simulant profondeur 2
        
        Args:
            game: Instance du jeu
            
        Returns:
            dict: Action à effectuer
        """
        # Générer toutes les actions possibles
        possible_actions = self.generate_actions(game, self.player)
        
        if not possible_actions or len(possible_actions) == 0:
            return {'type': 'pass'}
        
        # Filtrer l'action "pass" si d'autres actions existent
        non_pass_actions = [a for a in possible_actions if a['type'] != 'pass']
        if non_pass_actions:
            possible_actions = non_pass_actions
        
        best_action = None
        best_score = float('-inf')
        
        # Évaluer chaque action
        for action in possible_actions:
            # Simuler mon action
            sim_state = GameSimulator.copy_game_state(game)
            GameSimulator.simulate_action(sim_state, action)
            
            # Générer les réponses ennemies possibles
            enemy_actions = self.generate_actions(sim_state, self.enemy_player)
            
            # Limiter le nombre de réponses à évaluer (pour performance)
            if len(enemy_actions) > self.max_enemy_responses:
                enemy_actions = self.sample_best_actions(
                    sim_state, enemy_actions, self.max_enemy_responses
                )
            
            # Évaluer le pire cas (adversaire joue optimal)
            min_score = float('inf')
            
            if not enemy_actions or len(enemy_actions) == 0:
                # Si l'ennemi n'a pas d'actions, évaluer l'état directement
                min_score = evaluate_state(sim_state, self.player)
            else:
                for enemy_action in enemy_actions:
                    sim_state2 = GameSimulator.copy_game_state(sim_state)
                    GameSimulator.simulate_action(sim_state2, enemy_action)
                    
                    score = evaluate_state(sim_state2, self.player)
                    min_score = min(min_score, score)
            
            # Ajouter un petit bruit aléatoire pour briser les égalités
            min_score += random.uniform(-0.1, 0.1)
            
            # Choisir l'action qui maximise le score minimum (minimax)
            if min_score > best_score:
                best_score = min_score
                best_action = action
        
        return best_action if best_action else {'type': 'pass'}
    
    def generate_actions(self, game, player):
        """
        Génère toutes les actions légales pour un joueur
        
        Args:
            game: État du jeu
            player (int): Joueur dont on génère les actions
            
        Returns:
            list: Liste d'actions possibles
        """
        actions = []
        
        # Ressources du joueur
        steaks = game.player1_steaks if player == 1 else game.player2_steaks
        
        # 1. Actions de spawn (seulement si c'est le tour actuel du joueur)
        if player == game.current_player and not getattr(game, 'spawn_action_done', False):
            spawn_positions = self.calculate_spawn_positions(game, player)
            costs = {1: 40, 2: 80, 3: 100}
            
            for pos in spawn_positions:
                for dino_type in [1, 2, 3]:
                    if steaks >= costs[dino_type]:
                        # Vérifier le cooldown du spawn
                        cooldown_ok = True
                        if hasattr(game, 'spawn_cooldowns'):
                            cooldown = game.spawn_cooldowns.get(player, {}).get(dino_type, 0)
                            if cooldown > 0:
                                cooldown_ok = False
                        
                        if cooldown_ok:
                            actions.append({
                                'type': 'spawn',
                                'x': pos[0],
                                'y': pos[1],
                                'dino_type': dino_type
                            })
        
        # 2. Actions avec les dinosaures (seulement ceux qui n'ont pas bougé)
        for dino in game.dinosaurs:
            if dino.player == player and not dino.has_moved and dino.immobilized_turns == 0:
                # Mouvements
                moves = self.calculate_possible_moves(game, dino)
                for move_pos in moves:
                    actions.append({
                        'type': 'move',
                        'dinosaur': dino,
                        'target_x': move_pos[0],
                        'target_y': move_pos[1]
                    })
                
                # Attaques (toujours prioritaires si disponibles)
                targets = self.calculate_attack_targets(game, dino, player)
                for target, target_type in targets:
                    actions.append({
                        'type': 'attack',
                        'attacker': dino,
                        'target': target,
                        'target_type': target_type
                    })
        
        # 3. Passer le tour (toujours possible)
        actions.append({'type': 'pass'})
        
        return actions
    
    def calculate_spawn_positions(self, game, player):
        """Calcule les positions valides pour spawner"""
        positions = []
        egg = game.eggs[player]
        max_distance = 3
        
        for x in range(game.logic_width):
            for y in range(game.logic_height):
                # Vérifier la distance à l'œuf
                distance = abs(x - egg.x) + abs(y - egg.y)
                if distance <= max_distance:
                    # Vérifier que la case est libre
                    is_free = True
                    
                    # Vérifier œufs
                    for e in game.eggs.values():
                        if e.x == x and e.y == y:
                            is_free = False
                            break
                    
                    # Vérifier dinosaures
                    if is_free:
                        for d in game.dinosaurs:
                            if d.x == x and d.y == y:
                                is_free = False
                                break
                    
                    if is_free:
                        positions.append((x, y))
        
        return positions
    
    def calculate_possible_moves(self, game, dinosaur):
        """Calcule les déplacements possibles pour un dinosaure"""
        moves = []
        move_range = dinosaur.movement_range
        
        for dx in range(-move_range, move_range + 1):
            for dy in range(-move_range, move_range + 1):
                # Distance Manhattan
                if abs(dx) + abs(dy) <= move_range and (dx != 0 or dy != 0):
                    target_x = dinosaur.x + dx
                    target_y = dinosaur.y + dy
                    
                    # Vérifier que c'est dans les limites
                    if 0 <= target_x < game.logic_width and 0 <= target_y < game.logic_height:
                        # Vérifier que la case est libre
                        is_free = True
                        
                        # Vérifier œufs
                        for egg in game.eggs.values():
                            if egg.x == target_x and egg.y == target_y:
                                is_free = False
                                break
                        
                        # Vérifier dinosaures
                        if is_free:
                            for d in game.dinosaurs:
                                if d.x == target_x and d.y == target_y:
                                    is_free = False
                                    break
                        
                        if is_free:
                            moves.append((target_x, target_y))
        
        return moves
    
    def calculate_attack_targets(self, game, dinosaur, player):
        """Calcule les cibles attaquables (adjacentes)"""
        targets = []
        
        # Cases adjacentes (orthogonales uniquement)
        adjacent_positions = [
            (dinosaur.x - 1, dinosaur.y),
            (dinosaur.x + 1, dinosaur.y),
            (dinosaur.x, dinosaur.y - 1),
            (dinosaur.x, dinosaur.y + 1)
        ]
        
        for pos_x, pos_y in adjacent_positions:
            # Vérifier œuf ennemi
            enemy_player = 3 - player
            if enemy_player in game.eggs:
                egg = game.eggs[enemy_player]
                if egg.x == pos_x and egg.y == pos_y:
                    targets.append((egg, 'egg'))
            
            # Vérifier dinosaures ennemis
            for dino in game.dinosaurs:
                if dino.player != player and dino.x == pos_x and dino.y == pos_y:
                    targets.append((dino, 'dinosaur'))
        
        return targets
    
    def sample_best_actions(self, game_state, actions, n):
        """
        Échantillonne les n meilleures actions selon une heuristique greedy
        
        Args:
            game_state: État du jeu
            actions: Liste d'actions à échantillonner
            n: Nombre d'actions à garder
            
        Returns:
            list: Les n meilleures actions
        """
        if len(actions) <= n:
            return actions
        
        scored = []
        for action in actions:
            sim = GameSimulator.copy_game_state(game_state)
            GameSimulator.simulate_action(sim, action)
            score = evaluate_state(sim, self.enemy_player)
            scored.append((score, action))
        
        # Trier par meilleur score et prendre top-n
        scored.sort(reverse=True, key=lambda x: x[0])
        return [a for _, a in scored[:n]]
