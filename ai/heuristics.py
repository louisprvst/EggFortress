"""
Fonctions d'évaluation heuristique pour les états de jeu
"""

def evaluate_state(game_state, ai_player):
    """
    Évalue un état de jeu du point de vue du joueur IA
    
    Args:
        game_state: État du jeu à évaluer
        ai_player (int): Numéro du joueur IA (1 ou 2)
        
    Returns:
        float: Score de l'état (plus élevé = meilleur pour l'IA)
    """
    score = 0
    enemy_player = 3 - ai_player
    
    # Vérifier conditions de victoire/défaite
    if game_state.eggs[enemy_player].health <= 0:
        return 100000  # Victoire !
    if game_state.eggs[ai_player].health <= 0:
        return -100000  # Défaite !
    
    # 1. Santé des œufs (critère le plus important)
    score += game_state.eggs[ai_player].health * 10
    score -= game_state.eggs[enemy_player].health * 10
    
    # 2. Nombre et santé des dinosaures
    my_dinos = [d for d in game_state.dinosaurs if d.player == ai_player]
    enemy_dinos = [d for d in game_state.dinosaurs if d.player == enemy_player]
    
    score += len(my_dinos) * 50
    score -= len(enemy_dinos) * 50
    
    score += sum(d.health for d in my_dinos) * 2
    score -= sum(d.health for d in enemy_dinos) * 2
    
    # 3. Ressources (steaks) - léger bonus
    my_steaks = game_state.player1_steaks if ai_player == 1 else game_state.player2_steaks
    enemy_steaks = game_state.player1_steaks if enemy_player == 1 else game_state.player2_steaks
    score += my_steaks * 0.5
    score -= enemy_steaks * 0.5
    
    # 4. Proximité à l'œuf ennemi (pression offensive)
    egg_enemy = game_state.eggs[enemy_player]
    for dino in my_dinos:
        distance = abs(dino.x - egg_enemy.x) + abs(dino.y - egg_enemy.y)
        score -= distance * 3  # Récompenser proximité
    
    # 5. Protection de mon œuf (distance ennemis → mon œuf)
    egg_my = game_state.eggs[ai_player]
    for dino in enemy_dinos:
        distance = abs(dino.x - egg_my.x) + abs(dino.y - egg_my.y)
        score += distance * 2  # Pénaliser ennemis proches
    
    # 6. Bonus pour dinosaures de type fort près de l'objectif
    for dino in my_dinos:
        if dino.dino_type == 3:  # Tank
            dist_to_enemy_egg = abs(dino.x - egg_enemy.x) + abs(dino.y - egg_enemy.y)
            if dist_to_enemy_egg <= 2:
                score += 30  # Bonus pour tank près de l'œuf ennemi
    
    return score
