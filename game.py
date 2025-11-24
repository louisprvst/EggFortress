import pygame
from Entities.Dinosaur import Dinosaur
from Entities.Egg import Egg
from Entities.SpawnEgg import SpawnEgg
from Entities.Trap import Trap
from map_generator import MapGenerator
from ui import UI

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # États du jeu
        self.current_player = 1  # 1 pour bleu, 2 pour rouge
        self.turn_number = 1
        self.game_over = False
        self.winner = None
        
        # Ressources des joueurs
        self.player1_steaks = 100
        self.player2_steaks = 100
        
        # Entités du jeu
        self.eggs = {}
        self.dinosaurs = []
        self.traps = []
        self.spawn_eggs = []
        
        # Map
        self.map_generator = MapGenerator(width=16, height=12, visual_width=32, visual_height=24)
        self.grid = self.map_generator.generate_map()
        self.visual_base, self.visual_elements = self.map_generator.generate_visual_map()
        
        self.logic_width = 16
        self.logic_height = 12
        
        # Calculer la taille des cellules pour qu'elles soient carrées
        available_height = self.screen_height - 120
        
        cell_size_by_width = self.screen_width // self.logic_width
        cell_size_by_height = available_height // self.logic_height
        
        self.cell_size = min(cell_size_by_width, cell_size_by_height)
        
        self.logic_cell_width = self.cell_size
        self.logic_cell_height = self.cell_size
        
        self.visual_cell_width = self.cell_size
        self.visual_cell_height = self.cell_size
        
        self.visual_width = self.logic_width
        self.visual_height = self.logic_height
        
        self.board_width = self.logic_width * self.cell_size
        self.board_height = self.logic_height * self.cell_size
        self.board_offset_x = (self.screen_width - self.board_width) // 2
        self.board_offset_y = (available_height - self.board_height) // 2
        
        self.cell_width = self.logic_cell_width
        self.cell_height = self.logic_cell_height
        
        # UI
        self.ui = UI(self.screen)
        
        # Sélection
        self.selected_cell = None
        self.selected_dinosaur = None
        self.action_mode = None
        self.possible_moves = []
        self.attack_targets = []
        self.spawn_positions = []
        self.action_taken = False
        self.spawn_action_done = False
        
        # Système de cooldown pour spawner
        self.spawn_cooldowns = {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}}
        self.last_time = pygame.time.get_ticks()
        
        self.turn_time_limit = 120
        self.turn_start_time = pygame.time.get_ticks()
        self.auto_end_turn_time = None
        
        # Animation de déplacement
        self.moving_dinosaur = None
        self.move_animation = {
            'active': False,
            'dinosaur': None,
            'start_pos': None,
            'target_pos': None,
            'current_pos': None,
            'speed': 0,
            'progress': 0
        }
        
        self.turn_popup = {
            'active': False,
            'text': '',
            'timer': 0,
            'duration': 2.0
        }
        
        self.error_message = {
            'active': False,
            'text': '',
            'timer': 0,
            'duration': 2.5
        }
        
        self.kill_notification = {
            'active': False,
            'text': '',
            'timer': 0,
            'duration': 3.0
        }
        
        self.init_game()
    
    def init_game(self):
        """Initialise le jeu avec les œufs aux positions de base"""
        egg1_pos = (1,1)
        egg2_pos = (14,10)
        
        self.eggs[1] = Egg(egg1_pos[0], egg1_pos[1], 1)
        self.eggs[2] = Egg(egg2_pos[0], egg2_pos[1], 2)
    
    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.restart_game()
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                
                ui_height = 140
                attack_width = 140
                attack_height = 70
                attack_x = (self.screen_width - attack_width) // 2
                attack_y = self.screen_height - ui_height - attack_height - 20
                
                if (attack_x <= mouse_x <= attack_x + attack_width and 
                    attack_y <= mouse_y <= attack_y + attack_height):
                    if (self.selected_dinosaur and 
                        self.selected_dinosaur.player == self.current_player and 
                        not self.selected_dinosaur.has_moved and 
                        self.selected_dinosaur.immobilized_turns == 0 and
                        self.attack_targets):
                        self.action_mode = 'attack_mode'
                
                elif mouse_y > self.screen_height - 100:
                    self.handle_ui_click(mouse_x, mouse_y)
                else:
                    adjusted_x = mouse_x - self.board_offset_x
                    adjusted_y = mouse_y - self.board_offset_y
                    
                    grid_x = adjusted_x // self.cell_width
                    grid_y = adjusted_y // self.cell_height
                    
                    if 0 <= grid_x < self.logic_width and 0 <= grid_y < self.logic_height:
                        self.handle_grid_click(grid_x, grid_y)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.spawn_action_done:
                self.end_turn()
            elif event.key == pygame.K_ESCAPE:
                self.cancel_action()
    
    def handle_ui_click(self, mouse_x, mouse_y):
        """Gère les clics sur l'interface utilisateur"""
        # Nouvelle disposition UI : boutons centrés
        # Calculer les positions des boutons (correspond à la nouvelle UI)
        button_spacing = 125
        total_width = button_spacing * 4  # 3 dinos + 1 piège
        start_x = (self.screen_width - total_width) // 2 + 50
        button_y = self.screen_height - 140 + 20  # ui_height = 140, offset = 20
        button_width = 110
        button_height = 95
        
        # Coûts des dinosaures
        costs = {1: 40, 2: 80, 3: 100}
        current_steaks = self.player1_steaks if self.current_player == 1 else self.player2_steaks
        
        # Bouton Dino 1 (Rapide)
        btn1_x = start_x
        if btn1_x <= mouse_x <= btn1_x + button_width and button_y <= mouse_y <= button_y + button_height:
            cooldown = self.spawn_cooldowns[self.current_player][1]
            # Vérifier le cooldown
            if cooldown > 0:
                self.show_error_message(f" Cooldown actif: {int(cooldown)}s")
                return
            # Vérifier si assez de steaks
            if current_steaks < costs[1]:
                self.show_error_message(f" Pas assez de steaks ! ({current_steaks}/{costs[1]})")
                return
            self.action_mode = 'spawn'
            self.spawn_type = 1
            self.spawn_positions = self.calculate_spawn_positions()
        
        # Bouton Dino 2 (Équilibré)
        elif start_x + button_spacing <= mouse_x <= start_x + button_spacing + button_width and button_y <= mouse_y <= button_y + button_height:
            cooldown = self.spawn_cooldowns[self.current_player][2]
            # Vérifier le cooldown
            if cooldown > 0:
                self.show_error_message(f" Cooldown actif: {int(cooldown)}s")
                return
            # Vérifier si assez de steaks
            if current_steaks < costs[2]:
                self.show_error_message(f"Pas assez de steaks ! ({current_steaks}/{costs[2]})")
                return
            self.action_mode = 'spawn'
            self.spawn_type = 2
            self.spawn_positions = self.calculate_spawn_positions()
        
        # Bouton Dino 3 (Tank)
        elif start_x + button_spacing * 2 <= mouse_x <= start_x + button_spacing * 2 + button_width and button_y <= mouse_y <= button_y + button_height:
            cooldown = self.spawn_cooldowns[self.current_player][3]
            # Vérifier le cooldown
            if cooldown > 0:
                self.show_error_message(f" Cooldown actif: {int(cooldown)}s")
                return
            # Vérifier si assez de steaks
            if current_steaks < costs[3]:
                self.show_error_message(f" Pas assez de steaks ! ({current_steaks}/{costs[3]})")
                return
            self.action_mode = 'spawn'
            self.spawn_type = 3
            self.spawn_positions = self.calculate_spawn_positions()
        
        # Bouton Piège
        elif start_x + button_spacing * 3 <= mouse_x <= start_x + button_spacing * 3 + button_width and button_y <= mouse_y <= button_y + button_height:
            self.action_mode = 'trap'
    
    def handle_grid_click(self, grid_x, grid_y):
        """Gère les clics sur la grille de jeu"""
        if self.move_animation['active'] or self.spawn_action_done:
            return  # Animation en cours ou spawn déjà fait
            
        if self.action_mode == 'spawn' and hasattr(self, 'spawn_type'):
            # Vérifier si on peut spawner à cette position
            if (grid_x, grid_y) in self.spawn_positions:
                if self.spawn_dinosaur(grid_x, grid_y, self.spawn_type):
                    self.spawn_action_done = True  # Le tour se termine après un spawn
                    self.clear_selection()
                    # Terminer automatiquement le tour après 1 seconde
                    self.auto_end_turn_time = pygame.time.get_ticks() + 1000
        elif self.action_mode == 'trap':
            if self.place_trap(grid_x, grid_y):
                self.spawn_action_done = True  # Le tour se termine après un piège
                self.clear_selection()
                self.auto_end_turn_time = pygame.time.get_ticks() + 1000
        elif self.action_mode == 'attack_mode':
            target_found = False
            for target_type, tx, ty, target_entity in self.attack_targets:
                if tx == grid_x and ty == grid_y:
                    target_found = True
                    if target_type == 'dinosaur':
                        self.attack(self.selected_dinosaur, target_entity)
                    elif target_type == 'egg':
                        self.attack_egg(self.selected_dinosaur, target_entity)
                    
                    self.selected_dinosaur.has_moved = True
                    self.clear_selection()
                    self.check_victory()
                    break
                
        else:
            # Sélection d'un dinosaure ou attaque
            dino = self.get_dinosaur_at(grid_x, grid_y)
            
            if (dino and dino.player == self.current_player and 
                not dino.has_moved and 
                dino.immobilized_turns == 0):
                self.selected_dinosaur = dino
                self.selected_cell = (grid_x, grid_y)
                self.possible_moves = self.calculate_possible_moves(dino)
                self.attack_targets = self.calculate_attack_targets(dino)
                self.action_mode = 'move'
                
            elif self.selected_dinosaur and self.action_mode == 'move':
                if (grid_x, grid_y) in self.possible_moves:
                    if self.start_move_animation(self.selected_dinosaur, grid_x, grid_y):
                        pass
                        
                else:
                    self.clear_selection()
    
    def try_spawn_dinosaur(self, dino_type):
        """Tente de spawner un dinosaure si on a assez de steaks"""
        if self.action_taken:
            return  # Une seule action par tour
            
        costs = {1: 40, 2: 80, 3: 100}
        current_steaks = self.player1_steaks if self.current_player == 1 else self.player2_steaks
        
        if current_steaks >= costs[dino_type]:
            self.action_mode = 'spawn'
            self.spawn_type = dino_type
            self.clear_selection()
    
    def spawn_dinosaur(self, x, y, dino_type):
        """Spawne un œuf de dinosaure à la position donnée"""
        # Vérifier que la case est libre et proche de l'œuf du joueur
        if self.is_cell_free(x, y) and self.is_near_egg(x, y, self.current_player):
            costs = {1: 40, 2: 80, 3: 100}
            
            if self.current_player == 1:
                self.player1_steaks -= costs[dino_type]
            else:
                self.player2_steaks -= costs[dino_type]
            
            # Créer un œuf de spawn au lieu d'un dinosaure directement
            new_spawn_egg = SpawnEgg(x, y, self.current_player, dino_type)
            self.spawn_eggs.append(new_spawn_egg)
            
            # Démarrer le cooldown des boutons (plus court que les temps d'éclosion)
            cooldown_times = {1: 5, 2: 8, 3: 12}  # en secondes - cooldowns des boutons
            self.spawn_cooldowns[self.current_player][dino_type] = cooldown_times[dino_type]
            
            self.clear_selection()
            return True
        return False
    
    def place_trap(self, x, y):
        """Place un piège à la position donnée"""
        if self.is_cell_free(x, y):
            # Coût du piège (ajustez selon vos besoins)
            trap_cost = 30
            if self.current_player == 1:
                if self.player1_steaks >= trap_cost:
                    self.player1_steaks -= trap_cost
                else:
                    return False
            else:
                if self.player2_steaks >= trap_cost:
                    self.player2_steaks -= trap_cost
                else:
                    return False
            
            trap = Trap(x, y, self.current_player)
            self.traps.append(trap)
            self.clear_selection()
            return True
        return False
    
    def move_dinosaur(self, dinosaur, target_x, target_y):
        """Déplace un dinosaure vers la position cible"""
        if not dinosaur.has_moved and self.can_move_to(dinosaur, target_x, target_y):
            # Vérifier s'il y a un ennemi à attaquer
            target_dino = self.get_dinosaur_at(target_x, target_y)
            target_egg = self.get_egg_at(target_x, target_y)
            
            if target_dino and target_dino.player != dinosaur.player:
                self.attack(dinosaur, target_dino)
            elif target_egg and target_egg.player != dinosaur.player:
                self.attack_egg(dinosaur, target_egg)
            else:
                dinosaur.x = target_x
                dinosaur.y = target_y
            
            dinosaur.has_moved = True
            self.clear_selection()
            return True
        return False
    
    def calculate_possible_moves(self, dinosaur):
        """Calcule les mouvements possibles pour un dinosaure"""
        possible_moves = []
        for dx in range(-dinosaur.movement_range, dinosaur.movement_range + 1):
            for dy in range(-dinosaur.movement_range, dinosaur.movement_range + 1):
                if abs(dx) + abs(dy) <= dinosaur.movement_range and (dx != 0 or dy != 0):
                    new_x = dinosaur.x + dx
                    new_y = dinosaur.y + dy
                    if (0 <= new_x < 20 and 0 <= new_y < 15 and 
                        self.can_move_to(dinosaur, new_x, new_y)):
                        possible_moves.append((new_x, new_y))
        return possible_moves
    
    def calculate_attack_targets(self, dinosaur):
        """Calcule les cibles d'attaque possibles pour un dinosaure"""
        attack_targets = []
        
        # Portée d'attaque = 1 case (adjacent)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                target_x = dinosaur.x + dx
                target_y = dinosaur.y + dy
                
                if 0 <= target_x < self.logic_width and 0 <= target_y < self.logic_height:
                    # Vérifier s'il y a un dinosaure ennemi
                    target_dino = self.get_dinosaur_at(target_x, target_y)
                    if target_dino and target_dino.player != dinosaur.player:
                        attack_targets.append(('dinosaur', target_x, target_y, target_dino))
                    
                    # Vérifier s'il y a un œuf ennemi
                    target_egg = self.get_egg_at(target_x, target_y)
                    if target_egg and target_egg.player != dinosaur.player:
                        attack_targets.append(('egg', target_x, target_y, target_egg))
        
        return attack_targets
    
    def calculate_spawn_positions(self):
        """Calcule les positions où on peut spawner des dinosaures - version zoomée"""
        spawn_positions = []
        egg = self.eggs[self.current_player]
        
        for x in range(max(0, egg.x - 3), min(self.logic_width, egg.x + 4)):
            for y in range(max(0, egg.y - 3), min(self.logic_height, egg.y + 4)):
                distance = abs(egg.x - x) + abs(egg.y - y)
                if distance <= 3 and self.is_cell_free(x, y):
                    spawn_positions.append((x, y))
        
        return spawn_positions
    
    def show_turn_popup(self, message):
        """Affiche un pop-up pour les changements de tour"""
        self.turn_popup = {
            'active': True,
            'text': message,
            'timer': 0,
            'duration': 2.0
        }
    
    def update_turn_popup(self, delta_time):
        """Met à jour le pop-up de tour"""
        if self.turn_popup['active']:
            self.turn_popup['timer'] += delta_time
            if self.turn_popup['timer'] >= self.turn_popup['duration']:
                self.turn_popup['active'] = False
    
    def show_error_message(self, message):
        """Affiche un message d'erreur à l'écran"""
        self.error_message = {
            'active': True,
            'text': message,
            'timer': 0,
            'duration': 2.5
        }
    
    def update_error_message(self, delta_time):
        """Met à jour le message d'erreur"""
        if self.error_message['active']:
            self.error_message['timer'] += delta_time
            if self.error_message['timer'] >= self.error_message['duration']:
                self.error_message['active'] = False
    
    def show_kill_notification(self, killer_player, victim_type):
        """Affiche une notification d'élimination à l'écran"""
        player_colors = {1: "BLEU", 2: "ROUGE"}
        killer_name = player_colors[killer_player]
        
        if victim_type == 'dinosaur':
            message = f"{killer_name} A ÉLIMINÉ UN DINOSAURE !"
        else:
            message = f"{killer_name} A ATTAQUÉ L'OEUF !"
        
        self.kill_notification = {
            'active': True,
            'text': message,
            'timer': 0,
            'duration': 3.0
        }
    
    def update_kill_notification(self, delta_time):
        """Met à jour la notification d'élimination"""
        if self.kill_notification['active']:
            self.kill_notification['timer'] += delta_time
            if self.kill_notification['timer'] >= self.kill_notification['duration']:
                self.kill_notification['active'] = False
    
    def start_move_animation(self, dinosaur, target_x, target_y):
        """Démarre l'animation de déplacement d'un dinosaure"""
        if not self.can_move_to(dinosaur, target_x, target_y):
            return False
        
        # Vitesses différentes selon le type de dinosaure
        speed_map = {1: 8.0, 2: 5.0, 3: 3.0}  # Plus le nombre est haut, plus c'est rapide
        
        self.move_animation = {
            'active': True,
            'dinosaur': dinosaur,
            'start_pos': (dinosaur.x, dinosaur.y),
            'target_pos': (target_x, target_y),
            'current_pos': [float(dinosaur.x), float(dinosaur.y)],
            'speed': speed_map[dinosaur.dino_type],
            'progress': 0.0
        }
        
        return True
    
    def update_move_animation(self, delta_time):
        """Met à jour l'animation de déplacement"""
        if not self.move_animation['active']:
            return
        
        anim = self.move_animation
        dinosaur = anim['dinosaur']
        
        # Calculer la direction
        dx = anim['target_pos'][0] - anim['start_pos'][0]
        dy = anim['target_pos'][1] - anim['start_pos'][1]
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance == 0:
            self.finish_move_animation()
            return
        
        # Normaliser la direction
        dx_norm = dx / distance
        dy_norm = dy / distance
        
        # Déplacer selon la vitesse
        move_distance = anim['speed'] * delta_time
        anim['current_pos'][0] += dx_norm * move_distance
        anim['current_pos'][1] += dy_norm * move_distance
        
        # Vérifier si on a atteint la destination
        current_dx = anim['target_pos'][0] - anim['current_pos'][0]
        current_dy = anim['target_pos'][1] - anim['current_pos'][1]
        
        if (dx * current_dx + dy * current_dy) <= 0:  # Produit scalaire <= 0 = arrivé
            self.finish_move_animation()
    
    def finish_move_animation(self):
        """Termine l'animation de déplacement"""
        if not self.move_animation['active']:
            return
        
        anim = self.move_animation
        dinosaur = anim['dinosaur']
        target_x, target_y = anim['target_pos']
        
        # Effectuer le vrai déplacement
        old_x, old_y = dinosaur.x, dinosaur.y
        dinosaur.x = target_x
        dinosaur.y = target_y
        dinosaur.has_moved = True
        
        # Vérifier les pièges ennemis
        self.check_traps(dinosaur)
        
        # Réinitialiser l'animation
        self.move_animation['active'] = False
        self.clear_selection()
    
    def check_traps(self, dinosaur):
        """Vérifie si le dinosaure marche sur un piège ennemi"""
        for trap in self.traps[:]:
            # Le dinosaure marche sur un piège de l'adversaire
            if (trap.x == dinosaur.x and trap.y == dinosaur.y and 
                trap.player != dinosaur.player and not trap.activated):
                
                # Activer le piège
                trap.activated = True
                
                # Le dinosaure sera immobilisé pendant 2 tours
                dinosaur.immobilized_turns = 2
                
                # Retirer le piège
                self.traps.remove(trap)

                return
    
    def is_enemy_at(self, x, y, player):
        """Vérifie s'il y a un ennemi à cette position"""
        # Vérifier dinosaure ennemi
        dino = self.get_dinosaur_at(x, y)
        if dino and dino.player != player:
            return True
        
        # Vérifier œuf ennemi
        egg = self.get_egg_at(x, y)
        if egg and egg.player != player:
            return True
        
        return False
    
    def clear_selection(self):
        """Efface la sélection actuelle"""
        self.action_mode = None
        self.selected_dinosaur = None
        self.selected_cell = None
        self.possible_moves = []
        self.attack_targets = []
        self.spawn_positions = []
        if hasattr(self, 'spawn_type'):
            delattr(self, 'spawn_type')
    
    def attack(self, attacker, defender):
        """Gère le combat entre deux dinosaures - seul le défenseur prend des dégâts"""
        damage = attacker.attack_power
        defender.take_damage(damage)
        
        attacker.has_moved = True
        
        if defender.health <= 0:
            self.dinosaurs.remove(defender)
            self.show_kill_notification(attacker.player, 'dinosaur')
            if attacker.player == 1:
                self.player1_steaks += 20
            else:
                self.player2_steaks += 20
    
    def attack_egg(self, attacker, egg):
        """Attaque un œuf ennemi"""
        damage = attacker.attack_power
        egg.take_damage(damage)
        
        self.show_kill_notification(attacker.player, 'egg')
        
        attacker.has_moved = True
    
    def end_turn(self):
        """Termine le tour du joueur actuel"""
        # Donner des steaks au joueur
        if self.current_player == 1:
            self.player1_steaks += 20
        else:
            self.player2_steaks += 20

        # Mettre à jour les œufs de spawn
        for egg in self.spawn_eggs:
            egg.on_turn_end()
        
        # Réinitialiser les mouvements des dinosaures du joueur actuel
        for dino in self.dinosaurs:
            if dino.player == self.current_player:
                dino.has_moved = False
        
        # Changer de joueur
        old_player = self.current_player
        self.current_player = 2 if self.current_player == 1 else 1
        if self.current_player == 1:
            self.turn_number += 1
        
        # Réduire l'immobilisation des dinosaures du NOUVEAU joueur actuel
        # (ceux qui vont jouer maintenant)
        for dino in self.dinosaurs:
            if dino.player == self.current_player:
                if dino.immobilized_turns > 0:
                    dino.immobilized_turns -= 1

        
        # Afficher un beau pop-up de changement de tour
        player_colors = {1: "Bleu", 2: "Rouge"}
        new_player_color = player_colors[self.current_player]
        old_player_color = player_colors[old_player]
        
        popup_text = f"Tour {self.turn_number}\nAu tour du joueur {new_player_color} !"
        
        self.show_turn_popup(popup_text)
        
        # Réinitialiser les actions
        self.action_taken = False
        self.spawn_action_done = False
        self.auto_end_turn_time = None
        self.clear_selection()
        
        # Réinitialiser le timer du tour
        self.turn_start_time = pygame.time.get_ticks()
        
        # Vérifier les conditions de victoire
        self.check_victory()
    
    def restart_game(self):
        """Redémarre le jeu"""
        self.current_player = 1
        self.turn_number = 1
        self.game_over = False
        self.winner = None
        self.player1_steaks = 100
        self.player2_steaks = 100
        self.eggs = {}
        self.dinosaurs = []
        self.traps = []
        self.spawn_eggs = []  # Nettoyer aussi les œufs de spawn
        self.selected_cell = None
        self.selected_dinosaur = None
        self.action_mode = None
        self.possible_moves = []
        self.spawn_positions = []
        self.action_taken = False
        self.spawn_action_done = False
        self.spawn_cooldowns = {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}}
        self.turn_start_time = pygame.time.get_ticks()
        self.auto_end_turn_time = None
        
        self.move_animation = {
            'active': False,
            'dinosaur': None,
            'start_pos': None,
            'target_pos': None,
            'current_pos': None,
            'speed': 0,
            'progress': 0
        }
        
        # Générer une nouvelle carte
        self.grid = self.map_generator.generate_map()
        self.visual_base, self.visual_elements = self.map_generator.generate_visual_map()
        self.init_game()
    
    def cancel_action(self):
        """Annule l'action en cours"""
        self.clear_selection()
    
    def has_tree_at(self, x, y):
        """Vérifie s'il y a un arbre à cette position logique"""
        # Convertir les coordonnées logiques en coordonnées visuelles
        # Chaque case logique correspond à visual_width/logic_width cases visuelles
        visual_per_logic_x = self.visual_width / self.logic_width
        visual_per_logic_y = self.visual_height / self.logic_height
        
        # Vérifier toutes les cases visuelles correspondant à cette case logique
        visual_x_start = int(x * visual_per_logic_x)
        visual_x_end = int((x + 1) * visual_per_logic_x)
        visual_y_start = int(y * visual_per_logic_y)
        visual_y_end = int((y + 1) * visual_per_logic_y)
        
        # S'il y a un arbre dans n'importe quelle case visuelle de cette zone, la case est bloquée
        for vy in range(visual_y_start, visual_y_end):
            for vx in range(visual_x_start, visual_x_end):
                if vy < len(self.visual_elements) and vx < len(self.visual_elements[vy]):
                    if self.visual_elements[vy][vx] == 'tree':
                        return True
        return False
    
    def is_cell_free(self, x, y):
        """Vérifie si une case est libre"""
        # Vérifier s'il y a un arbre
        if self.has_tree_at(x, y):
            return False
        
        # Vérifier les œufs
        for egg in self.eggs.values():
            if egg.x == x and egg.y == y:
                return False
        
        # Vérifier les dinosaures
        for dino in self.dinosaurs:
            if dino.x == x and dino.y == y:
                return False
        
        # Vérifier les pièges
        for trap in self.traps:
            if trap.x == x and trap.y == y:
                return False
        
        # Vérifier les œufs de spawn
        for spawn_egg in self.spawn_eggs:
            if spawn_egg.x == x and spawn_egg.y == y:
                return False
        
        return True
    
    def is_near_egg(self, x, y, player):
        """Vérifie si une position est proche de l'œuf du joueur"""
        egg = self.eggs[player]
        distance = abs(egg.x - x) + abs(egg.y - y)
        return distance <= 3
    
    def can_move_to(self, dinosaur, x, y):
        """Vérifie si un dinosaure peut se déplacer vers une position"""
        # Vérifier qu'il n'y a pas d'arbre
        if self.has_tree_at(x, y):
            return False
        
        distance = abs(dinosaur.x - x) + abs(dinosaur.y - y)
        return distance <= dinosaur.movement_range
    
    def get_dinosaur_at(self, x, y):
        """Retourne le dinosaure à la position donnée"""
        for dino in self.dinosaurs:
            if dino.x == x and dino.y == y:
                return dino
        return None
    
    def get_egg_at(self, x, y):
        """Retourne l'œuf à la position donnée"""
        for egg in self.eggs.values():
            if egg.x == x and egg.y == y:
                return egg
        return None
    
    def check_victory(self):
        """Vérifie les conditions de victoire"""
        for player, egg in self.eggs.items():
            if egg.health <= 0:
                self.game_over = True
                self.winner = 2 if player == 1 else 1
                break
    
    def update(self):
        """Met à jour l'état du jeu"""
        # Gérer les cooldowns et le temps
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0  # en secondes
        self.last_time = current_time
        
        # Décrémenter les cooldowns
        for player in [1, 2]:
            for dino_type in [1, 2, 3]:
                if self.spawn_cooldowns[player][dino_type] > 0:
                    self.spawn_cooldowns[player][dino_type] = max(0, 
                        self.spawn_cooldowns[player][dino_type] - delta_time)
        
        # Gérer le timer du tour (2 minutes max)
        elapsed_time = (current_time - self.turn_start_time) / 1000.0
        if elapsed_time >= self.turn_time_limit:
            self.end_turn()
        
        # Vérifier si on doit terminer le tour automatiquement après spawn/piège
        if self.auto_end_turn_time and current_time >= self.auto_end_turn_time:
            self.end_turn()
        
        # Mettre à jour l'animation de déplacement
        self.update_move_animation(delta_time)
        
        # Mettre à jour les œufs de spawn
        spawn_eggs_to_remove = []
        for i, spawn_egg in enumerate(self.spawn_eggs):
            spawn_egg.update_spawn(delta_time)
            if spawn_egg.is_ready_to_hatch():
                # Créer le dinosaure et supprimer l'œuf
                new_dino = Dinosaur(spawn_egg.x, spawn_egg.y, spawn_egg.player, spawn_egg.dino_type)
                self.dinosaurs.append(new_dino)
                spawn_eggs_to_remove.append(i)
        
        # Supprimer les œufs éclos (en ordre inverse pour éviter les problèmes d'index)
        for i in reversed(spawn_eggs_to_remove):
            self.spawn_eggs.pop(i)
        
        # Mettre à jour le pop-up de tour
        self.update_turn_popup(delta_time)
        
        # Mettre à jour le message d'erreur
        self.update_error_message(delta_time)
        
        # Mettre à jour la notification d'élimination
        self.update_kill_notification(delta_time)
        
        # Vérifier les conditions de victoire
        if not self.game_over:
            self.check_victory()
    
    def draw(self):
        """Dessine le jeu"""
        self.screen.fill((50, 50, 50))
        
        # Dessiner la grille
        self.draw_grid()
        
        # Dessiner les entités
        self.draw_entities()
        
        # Dessiner l'UI
        self.ui.draw(self)
        
        # Dessiner les indications de sélection
        if self.selected_cell:
            self.draw_selection()
        
        # Dessiner les mouvements possibles
        self.draw_possible_moves()
        
        # Dessiner les cibles d'attaque possibles seulement en mode attaque
        if self.action_mode == 'attack_mode':
            self.draw_attack_targets()
            self.draw_attack_mode_instruction()
        
        # Dessiner les positions de spawn possibles
        self.draw_spawn_positions()
        
        # Dessiner le pop-up de changement de tour
        if self.turn_popup['active']:
            self.draw_turn_popup()
        
        # Dessiner le message d'erreur
        if self.error_message['active']:
            self.draw_error_message()
        
        # Dessiner la notification d'élimination (par-dessus tout)
        if self.kill_notification['active']:
            self.draw_kill_notification()
    
    def draw_grid(self):
        """Dessine la grille de jeu avec des cases carrées et des textures complètes"""
        # Dessiner chaque case avec sa texture
        for y in range(self.logic_height):
            for x in range(self.logic_width):
                # Position de la case (avec offset pour centrer)
                cell_x = self.board_offset_x + x * self.cell_size
                cell_y = self.board_offset_y + y * self.cell_size
                
                # Récupérer le terrain de base
                if y < len(self.visual_base) and x < len(self.visual_base[y]):
                    base_terrain = self.visual_base[y][x]
                    base_image = self.map_generator.get_terrain_image(base_terrain)
                    
                    if base_image:
                        # Redimensionner pour remplir toute la case carrée
                        scaled_image = pygame.transform.scale(base_image, (self.cell_size, self.cell_size))
                        self.screen.blit(scaled_image, (cell_x, cell_y))
                    else:
                        # Fallback avec couleur unie
                        color = self.get_terrain_color(base_terrain)
                        pygame.draw.rect(self.screen, color, 
                                       (cell_x, cell_y, self.cell_size, self.cell_size))
                
                # Dessiner les éléments par-dessus (arbres, fleurs, etc.)
                if y < len(self.visual_elements) and x < len(self.visual_elements[y]):
                    element_terrain = self.visual_elements[y][x]
                    
                    if element_terrain:
                        element_image = self.map_generator.get_terrain_image(element_terrain)
                        
                        if element_image:
                            scaled_image = pygame.transform.scale(element_image, 
                                                                (self.cell_size, self.cell_size))
                            self.screen.blit(scaled_image, (cell_x, cell_y))
                
                # Effet damier subtil pour la lisibilité
                if (x + y) % 2 == 0:
                    overlay = pygame.Surface((self.cell_size, self.cell_size))
                    overlay.set_alpha(15)
                    overlay.fill((255, 255, 255))
                    self.screen.blit(overlay, (cell_x, cell_y))
                
                # Bordure de case
                pygame.draw.rect(self.screen, (80, 80, 80), 
                               (cell_x, cell_y, self.cell_size, self.cell_size), 2)
        
        # Dessiner les lignes de grille principales pour plus de clarté
        for x in range(self.logic_width + 1):
            pygame.draw.line(self.screen, (40, 40, 40), 
                           (self.board_offset_x + x * self.cell_size, self.board_offset_y), 
                           (self.board_offset_x + x * self.cell_size, self.board_offset_y + self.board_height), 3)
        
        for y in range(self.logic_height + 1):
            pygame.draw.line(self.screen, (40, 40, 40), 
                           (self.board_offset_x, self.board_offset_y + y * self.cell_size), 
                           (self.board_offset_x + self.board_width, self.board_offset_y + y * self.cell_size), 3)
    
    def get_terrain_color(self, terrain_type):
        """Retourne une couleur de fallback pour chaque type de terrain"""
        terrain_colors = {
            'grass': (34, 139, 34),      # Vert herbe
            'dirt': (139, 69, 19),       # Marron terre
            'tree': (0, 100, 0),         # Vert foncé
            'bush': (50, 205, 50),       # Vert clair
            'flower': (255, 20, 147),    # Rose magenta
            'flower_2': (255, 69, 0),    # Rouge orangé
            'flower_3': (138, 43, 226),  # Violet
            'flower_4': (255, 215, 0)    # Jaune doré
        }
        return terrain_colors.get(terrain_type, (34, 139, 34))  # Défaut : vert herbe
    
    def draw_entities(self):
        """Dessine toutes les entités du jeu"""
        # Dessiner les œufs
        for egg in self.eggs.values():
            egg.draw(self.screen, self.cell_width, self.cell_height, self.board_offset_x, self.board_offset_y)
        
        # Dessiner les pièges (seulement visibles pour le joueur qui les a placés)
        for trap in self.traps:
            trap.draw(self.screen, self.cell_width, self.cell_height, self.current_player, self.board_offset_x, self.board_offset_y)
        
        # Dessiner les œufs de spawn
        for spawn_egg in self.spawn_eggs:
            spawn_egg.draw(self.screen, self.cell_width, self.cell_height, self.board_offset_x, self.board_offset_y)
        
        # Dessiner les dinosaures
        for dinosaur in self.dinosaurs:
            if self.move_animation['active'] and dinosaur == self.move_animation['dinosaur']:
                # Dessiner le dinosaure à sa position animée
                anim_x = self.board_offset_x + self.move_animation['current_pos'][0] * self.cell_width
                anim_y = self.board_offset_y + self.move_animation['current_pos'][1] * self.cell_height
                if dinosaur.image:
                    scaled_image = pygame.transform.scale(dinosaur.image, (int(self.cell_width), int(self.cell_height)))
                    self.screen.blit(scaled_image, (anim_x, anim_y))
            else:
                # Dessiner normalement
                dinosaur.draw(self.screen, self.cell_width, self.cell_height, self.board_offset_x, self.board_offset_y)
    
    def draw_selection(self):
        """Dessine la sélection actuelle"""
        if self.selected_cell:
            x, y = self.selected_cell
            rect = pygame.Rect(self.board_offset_x + x * self.cell_width, 
                             self.board_offset_y + y * self.cell_height, 
                             self.cell_width, self.cell_height)
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)
    
    def draw_possible_moves(self):
        """Dessine les cases où le dinosaure peut se déplacer en bleu"""
        for x, y in self.possible_moves:
            rect = pygame.Rect(self.board_offset_x + x * self.cell_width, 
                             self.board_offset_y + y * self.cell_height, 
                             self.cell_width, self.cell_height)
            # Surface semi-transparente bleue
            s = pygame.Surface((self.cell_width, self.cell_height))
            s.set_alpha(128)
            s.fill((0, 100, 255))
            self.screen.blit(s, (self.board_offset_x + x * self.cell_width, 
                               self.board_offset_y + y * self.cell_height))
            pygame.draw.rect(self.screen, (0, 150, 255), rect, 2)
    
    def draw_attack_targets(self):
        """Dessine les cibles d'attaque possibles en rouge avec animation de pulsation"""
        # Animation de pulsation
        pulse = abs(pygame.math.Vector2(0, 0).angle_to((1, 0))) 
        time_ms = pygame.time.get_ticks()
        pulse_alpha = int(100 + 100 * abs((time_ms % 1000) / 1000.0 - 0.5))
        
        for target_type, x, y, target_entity in self.attack_targets:
            rect = pygame.Rect(self.board_offset_x + x * self.cell_width, 
                             self.board_offset_y + y * self.cell_height, 
                             self.cell_width, self.cell_height)
            
            # Surface semi-transparente rouge pulsante pour les attaques
            s = pygame.Surface((self.cell_width, self.cell_height))
            s.set_alpha(pulse_alpha)
            s.fill((255, 50, 50))
            self.screen.blit(s, (self.board_offset_x + x * self.cell_width, 
                               self.board_offset_y + y * self.cell_height))
            
            # Bordure rouge épaisse
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 4)
            pygame.draw.rect(self.screen, (255, 255, 255), rect.inflate(-4, -4), 2)
            
            # Dessiner des cercles concentriques pour l'effet de cible
            center_x = self.board_offset_x + x * self.cell_width + self.cell_width // 2
            center_y = self.board_offset_y + y * self.cell_height + self.cell_height // 2
            
            # Cercles de cible
            pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), 20, 3)
            pygame.draw.circle(self.screen, (255, 100, 100), (center_x, center_y), 15, 2)
            
            # Croix centrale pour indiquer l'attaque
            size = 12
            pygame.draw.line(self.screen, (255, 255, 255), 
                           (center_x - size, center_y), 
                           (center_x + size, center_y), 4)
            pygame.draw.line(self.screen, (255, 255, 255), 
                           (center_x, center_y - size), 
                           (center_x, center_y + size), 4)
            
            # Indicateur du type de cible
            font = pygame.font.Font(None, 20)
            if target_type == 'dinosaur':
                indicator = font.render("🦖", True, (255, 255, 255))
            else:
                indicator = font.render("🥚", True, (255, 255, 255))
            indicator_rect = indicator.get_rect(center=(center_x, center_y + self.cell_height // 2 - 10))
            self.screen.blit(indicator, indicator_rect)
    
    def draw_attack_mode_instruction(self):
        """Affiche un message indiquant de cliquer sur une cible"""
        width = 400
        height = 60
        x = (self.screen_width - width) // 2
        y = 30
        
        instruction_surface = pygame.Surface((width, height))
        instruction_surface.set_alpha(230)
        instruction_surface.fill((255, 100, 0))
        self.screen.blit(instruction_surface, (x, y))
        
        pygame.draw.rect(self.screen, (255, 150, 50), (x, y, width, height), 4)
        pygame.draw.rect(self.screen, (255, 255, 255), (x + 2, y + 2, width - 4, height - 4), 2)
        
        font = pygame.font.Font(None, 32)
        text = font.render("CLIQUEZ SUR UNE CIBLE POUR ATTAQUER", True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        
        shadow = font.render("CLIQUEZ SUR UNE CIBLE POUR ATTAQUER", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)
    
    def draw_spawn_positions(self):
        """Dessine les positions de spawn possibles en bleu"""
        for x, y in self.spawn_positions:
            rect = pygame.Rect(self.board_offset_x + x * self.cell_width, 
                             self.board_offset_y + y * self.cell_height, 
                             self.cell_width, self.cell_height)
            # Surface semi-transparente bleue
            s = pygame.Surface((self.cell_width, self.cell_height))
            s.set_alpha(100)
            s.fill((0, 255, 100))
            self.screen.blit(s, (self.board_offset_x + x * self.cell_width, 
                               self.board_offset_y + y * self.cell_height))
            pygame.draw.rect(self.screen, (0, 255, 150), rect, 2)
    
    def draw_turn_popup(self):
        """Dessine le pop-up de changement de tour"""
        # Animation d'échelle selon le temps
        progress = self.turn_popup['timer'] / self.turn_popup['duration']
        if progress < 0.2:
            scale = progress / 0.2  # Apparition
        elif progress > 0.8:
            scale = 1.0 - (progress - 0.8) / 0.2  # Disparition
        else:
            scale = 1.0  # Stable
        
        if scale <= 0:
            return
        
        # Dimensions et position
        base_width = 400
        base_height = 150
        width = int(base_width * scale)
        height = int(base_height * scale)
        
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2 - 50  # Un peu plus haut
        
        # Fond avec dégradé
        popup_surface = pygame.Surface((width, height))
        popup_surface.set_alpha(220)
        
        # Couleur selon le joueur actuel
        if self.current_player == 1:
            color1 = (20, 50, 120)
            color2 = (50, 100, 200)
            border_color = (100, 150, 255)
        else:
            color1 = (120, 20, 50)
            color2 = (200, 50, 100)
            border_color = (255, 100, 150)
        
        # Remplir avec dégradé simple
        for i in range(height):
            ratio = i / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(popup_surface, (r, g, b), (0, i), (width, i))
        
        self.screen.blit(popup_surface, (x, y))
        
        # Bordure brillante
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 4)
        pygame.draw.rect(self.screen, (255, 255, 255), (x + 2, y + 2, width - 4, height - 4), 2)
        
        # Texte
        font = pygame.font.Font(None, int(36 * scale))
        small_font = pygame.font.Font(None, int(28 * scale))
        
        lines = self.turn_popup['text'].split('\n')
        line_height = int(40 * scale)
        total_text_height = len(lines) * line_height
        start_y = y + (height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            if i == 0:
                text = font.render(line, True, (255, 255, 255))
            else:
                text = small_font.render(line, True, (255, 255, 255))
            
            text_rect = text.get_rect(center=(x + width // 2, start_y + i * line_height))
            
            # Ombre du texte
            shadow = font.render(line, True, (0, 0, 0)) if i == 0 else small_font.render(line, True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
            self.screen.blit(shadow, shadow_rect)
            
            # Texte principal
            self.screen.blit(text, text_rect)
    
    def draw_error_message(self):
        """Dessine le message d'erreur en haut de l'écran"""
        # Animation d'échelle selon le temps
        progress = self.error_message['timer'] / self.error_message['duration']
        if progress < 0.2:
            scale = progress / 0.2  # Apparition
        elif progress > 0.8:
            scale = 1.0 - (progress - 0.8) / 0.2  # Disparition
        else:
            scale = 1.0  # Stable
        
        if scale <= 0:
            return
        
        # Dimensions et position (en haut de l'écran)
        base_width = 550
        base_height = 90
        width = int(base_width * scale)
        height = int(base_height * scale)
        
        x = (self.screen_width - width) // 2
        y = 100  # Position fixe en haut
        
        # Fond avec dégradé rouge (erreur)
        popup_surface = pygame.Surface((width, height))
        popup_surface.set_alpha(240)
        
        # Couleur rouge pour les erreurs
        color1 = (139, 0, 0)    # Rouge foncé
        color2 = (220, 20, 60)  # Crimson
        border_color = (255, 69, 0)  # Rouge-orange
        
        # Remplir avec dégradé simple
        for i in range(height):
            ratio = i / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(popup_surface, (r, g, b), (0, i), (width, i))
        
        self.screen.blit(popup_surface, (x, y))
        
        # Bordure brillante
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 5)
        pygame.draw.rect(self.screen, (255, 255, 255), (x + 3, y + 3, width - 6, height - 6), 2)
        
        # Texte
        font = pygame.font.Font(None, int(40 * scale))
        text = font.render(self.error_message['text'], True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        
        # Ombre du texte
        shadow = font.render(self.error_message['text'], True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))
        self.screen.blit(shadow, shadow_rect)
        
        # Texte principal
        self.screen.blit(text, text_rect)
    
    def draw_kill_notification(self):
        """Dessine la notification d'élimination au centre de l'écran"""
        # Animation d'échelle selon le temps
        progress = self.kill_notification['timer'] / self.kill_notification['duration']
        if progress < 0.15:
            scale = progress / 0.15  # Apparition rapide
        elif progress > 0.85:
            scale = 1.0 - (progress - 0.85) / 0.15  # Disparition rapide
        else:
            scale = 1.0  # Stable
        
        if scale <= 0:
            return
        
        # Effet de pulsation
        pulse = 1.0 + 0.1 * abs((progress * 10) % 2 - 1)
        final_scale = scale * pulse
        
        # Dimensions et position (centre de l'écran)
        base_width = 700
        base_height = 120
        width = int(base_width * final_scale)
        height = int(base_height * final_scale)
        
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        
        # Fond avec dégradé doré/orange (élimination)
        popup_surface = pygame.Surface((width, height))
        popup_surface.set_alpha(250)
        
        # Couleur dorée/orange pour les éliminations
        color1 = (180, 50, 0)    # Orange foncé
        color2 = (255, 140, 0)   # Orange doré
        border_color = (255, 215, 0)  # Or
        
        # Remplir avec dégradé
        for i in range(height):
            ratio = i / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(popup_surface, (r, g, b), (0, i), (width, i))
        
        self.screen.blit(popup_surface, (x, y))
        
        # Bordures multiples pour effet brillant
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 6)
        pygame.draw.rect(self.screen, (255, 255, 255), (x + 4, y + 4, width - 8, height - 8), 3)
        pygame.draw.rect(self.screen, (255, 200, 0), (x + 8, y + 8, width - 16, height - 16), 2)
        
        # Texte avec effet gras
        font = pygame.font.Font(None, int(50 * final_scale))
        text = font.render(self.kill_notification['text'], True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        
        # Ombre du texte (multiple pour effet 3D)
        for offset in [(4, 4), (3, 3), (2, 2)]:
            shadow = font.render(self.kill_notification['text'], True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(text_rect.centerx + offset[0], text_rect.centery + offset[1]))
            self.screen.blit(shadow, shadow_rect)
        
        # Texte principal
        self.screen.blit(text, text_rect)