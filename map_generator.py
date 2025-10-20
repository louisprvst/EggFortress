import pygame
import random
import os

class MapGenerator:
    def __init__(self, width=16, height=12, visual_width=32, visual_height=24):
        """Initialise le générateur de map avec des assets terrain - plus de cases plus petites"""
        self.width = width  # Grille logique avec plus de cases
        self.height = height
        self.visual_width = visual_width  # Grille visuelle avec plus de détails
        self.visual_height = visual_height
        
        # Charger les assets de la carte
        self.terrain_images = self.load_terrain_assets()
        
    def load_terrain_assets(self):
        """Charge tous les assets de terrain disponibles"""
        assets = {}
        asset_path = "assets/map/"
        
        terrain_files = {
            'grass': 'grass.png',
            'dirt': 'dirt.png',
            'tree': 'tree.png',
            'bush': 'bush.png',
            'flower': 'flower.png',
            'flower_2': 'flower_2.png',
            'flower_3': 'flower_3.png',
            'flower_4': 'flower_4.png'
        }
        
        for terrain_type, filename in terrain_files.items():
            try:
                full_path = os.path.join(asset_path, filename)
                image = pygame.image.load(full_path)
                assets[terrain_type] = image
            except Exception as e:
                print(f"Impossible de charger {filename}: {e}")
                assets[terrain_type] = None
        
        return assets
    
    def generate_map(self):
        """Génère une carte logique simple"""
        # Grille logique simple 20x15 (toutes cases accessibles)
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append('grass')  # Toutes les cases sont accessibles
            grid.append(row)
        return grid
    
    def generate_beautiful_visual_map(self):
        """Génère une belle carte visuelle 32x24 avec design simple et épuré - plus de cases"""
        grid = []
        
        # Créer une carte simple avec principalement de l'herbe et un chemin de terre central
        for y in range(self.visual_height):
            row = []
            for x in range(self.visual_width):
                # Chemin de terre horizontal au centre (lignes 11-13)
                if 11 <= y <= 13:
                    terrain = 'dirt'
                # Chemin de terre vertical au centre (colonnes 15-17)
                elif 15 <= x <= 17:
                    terrain = 'dirt'
                # Quelques arbres très rares dans les coins (seulement 4 par coin)
                elif (x <= 2 and y <= 2) or (x >= 29 and y <= 2) or (x <= 2 and y >= 21) or (x >= 29 and y >= 21):
                    if random.random() < 0.15:  # 15% de chance d'avoir un arbre dans les coins
                        terrain = 'tree'
                    else:
                        terrain = 'grass'
                # Quelques buissons très rares (dispersés)
                elif (x == 6 and y == 4) or (x == 25 and y == 4) or (x == 6 and y == 19) or (x == 25 and y == 19) or (x == 10 and y == 8) or (x == 21 and y == 8) or (x == 10 and y == 15) or (x == 21 and y == 15):
                    terrain = 'bush'
                # Quelques fleurs très rares (parsemées)
                elif (x == 4 and y == 7) or (x == 27 and y == 7) or (x == 12 and y == 3) or (x == 19 and y == 3) or (x == 12 and y == 20) or (x == 19 and y == 20) or (x == 8 and y == 18) or (x == 23 and y == 18) or (x == 8 and y == 5) or (x == 23 and y == 5):
                    if random.random() < 0.7:  # 70% de chance d'avoir une fleur
                        terrain = random.choice(['flower', 'flower_2'])
                    else:
                        terrain = 'grass'
                # Tout le reste est de l'herbe
                else:
                    terrain = 'grass'
                
                row.append(terrain)
            grid.append(row)
        
        return grid
    
    def generate_visual_map(self):
        """Génère une grille visuelle détaillée avec couches séparées"""
        # Créer deux grilles visuelles : base et éléments
        visual_base = []  # Herbe et terre uniquement (fond)
        visual_elements = []  # Arbres, fleurs, buissons (premier plan)
        
        # Génération de la belle carte visuelle
        beautiful_map = self.generate_beautiful_visual_map()
        
        # Séparer en deux couches
        for row in beautiful_map:
            base_row = []
            elements_row = []
            
            for terrain in row:
                if terrain in ['grass', 'dirt']:
                    # Base layer
                    base_row.append(terrain)
                    elements_row.append(None)  # Pas d'élément par-dessus
                else:
                    # Element layer - mettre de l'herbe en base
                    base_row.append('grass')
                    elements_row.append(terrain)
            
            visual_base.append(base_row)
            visual_elements.append(elements_row)
        
        return visual_base, visual_elements
    
    def get_terrain_image(self, terrain_type):
        """Retourne l'image correspondant au type de terrain"""
        return self.terrain_images.get(terrain_type, None)