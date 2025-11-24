"""
Classe de base abstraite pour toutes les IA
"""

from abc import ABC, abstractmethod

class BaseAI(ABC):
    """Classe abstraite pour les agents IA"""
    
    def __init__(self, player):
        """
        Initialise l'agent IA
        
        Args:
            player (int): Numéro du joueur (1 ou 2)
        """
        self.player = player
        self.enemy_player = 3 - player
    
    @abstractmethod
    def choose_action(self, game):
        """
        Choisit une action à effectuer
        
        Args:
            game: Instance du jeu
            
        Returns:
            dict: Action à effectuer avec format {'type': ..., ...}
        """
        pass
