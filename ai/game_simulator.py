"""
Simulateur d'état de jeu pour l'IA
Permet de copier et simuler des actions sans affecter le jeu réel
"""

from Entities.Dinosaur import Dinosaur
from Entities.Trap import Trap

class GameSimulator:
    """Permet de copier et simuler des états de jeu"""
    
    @staticmethod
    def copy_game_state(game):
        """
        Crée une copie profonde de l'état du jeu
        
        Args:
            game: Instance du jeu à copier
            
        Returns:
            Game: Copie de l'état du jeu
        """
        # Créer une copie superficielle de base
        sim = type('GameState', (), {})()
        
        # Copier les références nécessaires (pas les objets pygame)
        sim.screen = game.screen
        sim.logic_width = game.logic_width
        sim.logic_height = game.logic_height
        
        # Copier les structures de données importantes manuellement
        # Pour éviter les problèmes avec pygame.Surface
        sim.eggs = {}
        for player, egg in game.eggs.items():
            new_egg = type('Egg', (), {})()
            new_egg.x = egg.x
            new_egg.y = egg.y
            new_egg.player = egg.player
            new_egg.health = egg.health
            new_egg.max_health = egg.max_health
            new_egg.take_damage = egg.take_damage
            sim.eggs[player] = new_egg
        
        # Copier les dinosaures
        sim.dinosaurs = []
        for dino in game.dinosaurs:
            new_dino = type('Dinosaur', (), {})()
            new_dino.x = dino.x
            new_dino.y = dino.y
            new_dino.player = dino.player
            new_dino.dino_type = dino.dino_type
            new_dino.health = dino.health
            new_dino.max_health = dino.max_health
            new_dino.attack_power = dino.attack_power
            new_dino.movement_range = dino.movement_range
            new_dino.has_moved = dino.has_moved
            new_dino.immobilized_turns = dino.immobilized_turns
            new_dino.take_damage = dino.take_damage
            sim.dinosaurs.append(new_dino)
        
        # Copier les pièges
        sim.traps = []
        for trap in game.traps:
            new_trap = type('Trap', (), {})()
            new_trap.x = trap.x
            new_trap.y = trap.y
            new_trap.player = trap.player
            sim.traps.append(new_trap)
        
        # Copier la grille
        sim.grid = [row[:] for row in game.grid] if hasattr(game, 'grid') else []
        
        # Copier les spawn_eggs
        sim.spawn_eggs = []
        for spawn_egg in game.spawn_eggs:
            new_spawn = type('SpawnEgg', (), {})()
            new_spawn.x = spawn_egg.x
            new_spawn.y = spawn_egg.y
            new_spawn.player = spawn_egg.player
            new_spawn.dino_type = spawn_egg.dino_type
            sim.spawn_eggs.append(new_spawn)
        
        # Copier les ressources
        sim.player1_steaks = game.player1_steaks
        sim.player2_steaks = game.player2_steaks
        sim.current_player = game.current_player
        sim.turn_number = game.turn_number
        
        return sim
    
    @staticmethod
    def simulate_action(game_state, action):
        """
        Applique une action sur un état de jeu simulé
        
        Args:
            game_state: État du jeu
            action (dict): Action à simuler avec format {'type': ..., ...}
            
        Returns:
            Game: État du jeu après l'action
        """
        action_type = action['type']
        
        try:
            if action_type == 'spawn':
                # Faire spawn un dinosaure
                x, y, dino_type = action['x'], action['y'], action['dino_type']
                GameSimulator._simulate_spawn(game_state, x, y, dino_type)
            
            elif action_type == 'move':
                # Déplacer un dinosaure
                dinosaur = action['dinosaur']
                target_x, target_y = action['target_x'], action['target_y']
                GameSimulator._simulate_move(game_state, dinosaur, target_x, target_y)
            
            elif action_type == 'attack':
                # Attaquer un ennemi
                attacker = action['attacker']
                target = action['target']
                target_type = action.get('target_type', 'dinosaur')
                GameSimulator._simulate_attack(game_state, attacker, target, target_type)
            
            elif action_type == 'trap':
                # Placer un piège
                x, y = action['x'], action['y']
                GameSimulator._simulate_trap(game_state, x, y)
            
            # 'pass' = ne rien faire, passer son tour
            
        except Exception as e:
            print(f"Erreur simulation: {e}")
        
        return game_state
    
    @staticmethod
    def _simulate_spawn(game_state, x, y, dino_type):
        """Simule le spawn d'un dinosaure"""
        costs = {1: 40, 2: 80, 3: 100}
        cost = costs[dino_type]
        
        # Déduire le coût
        if game_state.current_player == 1:
            game_state.player1_steaks -= cost
        else:
            game_state.player2_steaks -= cost
        
        # Créer le dinosaure
        new_dino = Dinosaur(x, y, game_state.current_player, dino_type)
        new_dino.has_moved = True  # Le dinosaure vient d'être spawné
        game_state.dinosaurs.append(new_dino)
    
    @staticmethod
    def _simulate_move(game_state, dinosaur, target_x, target_y):
        """Simule le déplacement d'un dinosaure"""
        # Trouver le dinosaure dans la copie
        for dino in game_state.dinosaurs:
            if (dino.x == dinosaur.x and dino.y == dinosaur.y and 
                dino.player == dinosaur.player and dino.dino_type == dinosaur.dino_type):
                dino.x = target_x
                dino.y = target_y
                dino.has_moved = True
                
                # Vérifier les pièges
                for trap in game_state.traps:
                    if trap.x == target_x and trap.y == target_y and trap.player != dino.player:
                        dino.take_damage(50)
                        dino.immobilized_turns = 2
                        game_state.traps.remove(trap)
                        break
                
                # Retirer si mort
                if dino.health <= 0:
                    game_state.dinosaurs.remove(dino)
                break
    
    @staticmethod
    def _simulate_attack(game_state, attacker, target, target_type):
        """Simule une attaque"""
        # Trouver l'attaquant dans la copie
        att_copy = None
        for dino in game_state.dinosaurs:
            if (dino.x == attacker.x and dino.y == attacker.y and 
                dino.player == attacker.player and dino.dino_type == attacker.dino_type):
                att_copy = dino
                break
        
        if not att_copy:
            return
        
        if target_type == 'egg':
            # Attaquer un œuf
            egg = game_state.eggs[target.player]
            egg.take_damage(att_copy.attack_power)
            att_copy.has_moved = True
        else:
            # Attaquer un dinosaure
            def_copy = None
            for dino in game_state.dinosaurs:
                if (dino.x == target.x and dino.y == target.y and 
                    dino.player == target.player and dino.dino_type == target.dino_type):
                    def_copy = dino
                    break
            
            if def_copy:
                def_copy.take_damage(att_copy.attack_power)
                att_copy.has_moved = True
                
                # Retirer si mort et donner bonus
                if def_copy.health <= 0:
                    game_state.dinosaurs.remove(def_copy)
                    if att_copy.player == 1:
                        game_state.player1_steaks += 20
                    else:
                        game_state.player2_steaks += 20
    
    @staticmethod
    def _simulate_trap(game_state, x, y):
        """Simule la pose d'un piège"""
        trap = Trap(x, y, game_state.current_player)
        game_state.traps.append(trap)
        
        # Déduire le coût (si défini)
        trap_cost = 30
        if game_state.current_player == 1:
            game_state.player1_steaks -= trap_cost
        else:
            game_state.player2_steaks -= trap_cost
