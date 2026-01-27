"""
Système de logging centralisé pour EggFortress
Crée un fichier de log par jour avec seulement les infos importantes et les erreurs
"""

import logging
import os
from datetime import datetime


class GameLogger:
    """Gestionnaire centralisé des logs du jeu"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pour avoir une seule instance de logger"""
        if cls._instance is None:
            cls._instance = super(GameLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialise le système de logging"""
        if GameLogger._initialized:
            return
        
        # Créer le dossier logs s'il n'existe pas
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Nom du fichier log avec seulement la date (quotidien)
        log_date = datetime.now().strftime('%Y%m%d')
        log_filename = f"eggfortress_{log_date}.log"
        log_path = os.path.join(self.log_dir, log_filename)
        
        # Vérifier si le fichier existe déjà
        file_exists = os.path.exists(log_path)
        
        # Configuration du logger principal
        self.logger = logging.getLogger('EggFortress')
        self.logger.setLevel(logging.INFO)  # INFO au lieu de DEBUG
        
        # Éviter les doublons de handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Format des logs simplifié
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s [%(name)s] %(message)s',
            datefmt='%H:%M:%S'  # Seulement l'heure
        )
        
        # Handler pour fichier (mode append pour log quotidien)
        file_handler = logging.FileHandler(
            log_path,
            mode='a',  # Append mode
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)  # INFO et plus
        file_handler.setFormatter(formatter)
        
        # Handler pour console (seulement warnings et erreurs)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        
        # Ajouter les handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Header de session seulement si nouveau fichier
        if not file_exists:
            self.logger.info("=" * 60)
            self.logger.info(f"EggFortress - {datetime.now().strftime('%d/%m/%Y')}")
            self.logger.info("=" * 60)
        else:
            self.logger.info(f"--- Nouvelle session {datetime.now().strftime('%H:%M:%S')} ---")
        
        # Loggers spécialisés
        self.game_logger = logging.getLogger('EggFortress.Game')
        self.ai_logger = logging.getLogger('EggFortress.AI')
        self.ui_logger = logging.getLogger('EggFortress.UI')
        self.menu_logger = logging.getLogger('EggFortress.Menu')
        self.assets_logger = logging.getLogger('EggFortress.Assets')
        
        GameLogger._initialized = True
    
    def get_logger(self, component=None):
        """Retourne le logger approprié selon le composant"""
        if component == "game":
            return self.game_logger
        elif component == "ai":
            return self.ai_logger
        elif component == "ui":
            return self.ui_logger
        elif component == "menu":
            return self.menu_logger
        elif component == "assets":
            return self.assets_logger
        else:
            return self.logger
    
    @staticmethod
    def cleanup_old_logs(days=30):
        """Supprime les logs de plus de X jours (par défaut 30 jours)"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            return
        
        now = datetime.now()
        deleted = 0
        for filename in os.listdir(log_dir):
            if filename.endswith('.log') and filename.startswith('eggfortress_'):
                filepath = os.path.join(log_dir, filename)
                try:
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    if (now - file_time).days > days:
                        os.remove(filepath)
                        deleted += 1
                except Exception as e:
                    logging.error(f"Erreur lors de la suppression de {filename}: {e}")
        
        if deleted > 0:
            logging.info(f"Nettoyage: {deleted} ancien(s) fichier(s) de log supprimé(s)")


# Instance globale du logger
_game_logger_instance = GameLogger()


def get_logger(component=None):
    """
    Fonction helper pour obtenir un logger
    
    Args:
        component: Type de composant ("game", "ai", "ui", "menu", "assets")
    
    Returns:
        Logger configuré
    """
    return _game_logger_instance.get_logger(component)
