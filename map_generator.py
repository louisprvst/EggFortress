import pygame
import random
import os

class MapGenerator:
    def __init__(self, width=16, height=12, visual_width=32, visual_height=24, map_name="default"):
        """Initialise le générateur de map avec des assets terrain - plus de cases plus petites"""
        self.width = width  # Grille logique avec plus de cases
        self.height = height
        self.visual_width = visual_width  # Grille visuelle avec plus de détails
        self.visual_height = visual_height
        self.map_name = map_name
        
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
        """Génère une belle carte visuelle selon le type de map sélectionné"""
        if self.map_name == "empty":
            return self.flat_map()
        elif self.map_name == "custom":
            return self.maze_map()
        else:  # "default"
            return self.default_map()
    
    def flat_map(self):
        """Génère une map vide avec uniquement de l'herbe"""
        grid = []
        for y in range(self.visual_height):
            row = []
            for x in range(self.visual_width):
                row.append('grass')
            grid.append(row)
        return grid
    
    def default_map(self):
        """Génère la map par défaut avec de l'herbe et quelques arbres à des positions fixes"""
        grid = []
        
        # Créer une carte avec de l'herbe partout
        for y in range(self.visual_height):
            row = []
            for x in range(self.visual_width):
                row.append('grass')
            grid.append(row)
        
        # Configuration personnalisée de la map
        # Types disponibles: 'tree', 'bush', 'dirt'
        custom_elements = [
            # Terre
            (6, 4, 'dirt'),
            (7, 4, 'dirt'),
            (5, 5, 'dirt'),
            (6, 5, 'dirt'),
            (7, 5, 'dirt'),
            (8, 5, 'dirt'),
            (5, 6, 'dirt'),
            (6, 6, 'dirt'),
            (6, 7, 'dirt'),
            (7, 6, 'dirt'),
            (8, 6, 'dirt'),
            (7, 7, 'dirt'),
            (8, 7, 'dirt'),
            (9, 7, 'dirt'),
            (7, 3, 'dirt'),
            (8, 4, 'dirt'),
            (9, 5, 'dirt'),
            (7, 8, 'dirt'),
            # Arbres
            (3, 3, 'tree'),
            (10, 5, 'tree'),
            (2, 8, 'tree'),
            (13, 2, 'tree'),
            (7, 1, 'tree'),
            (8, 10, 'tree'),
            # Buissons
            (0, 4, 'bush'),
            (12, 4, 'bush'),
            (4, 9, 'bush'),
            (14, 6, 'bush'),
            (11, 9, 'bush'),
        ]
        
        # Placer tous les éléments personnalisés
        for x, y, terrain_type in custom_elements:
            if 0 <= x < self.visual_width and 0 <= y < self.visual_height:
                grid[y][x] = terrain_type
        
        return grid
    
    def maze_map(self):
        """Génère une map personnalisée"""
        grid = []
        
        # Créer une carte avec de l'herbe partout
        for y in range(self.visual_height):
            row = []
            for x in range(self.visual_width):
                row.append('grass')
            grid.append(row)
        
        # Carré central avec ouvertures
        for y in range(4, 8):
            for x in range(6, 10):
                if y == 4 or y == 7 or x == 6 or x == 9:
                    if not ((x == 6 and y == 5) or (x == 9 and y == 6)):
                        grid[y][x] = 'tree'
        
        # Ligne horizontale gauche (y=6, x=3 à 5)
        for x in range(3, 6):
            grid[6][x] = 'tree'
        
        # Ligne horizontale haut droite (y=5, x=10 à 12)
        for x in range(10, 13):
            grid[5][x] = 'tree'
        
        # Ligne verticale gauche (y=4 à 5, x=4)
        for y in range(4, 6):
            grid[y][4] = 'tree'
        
        # Ligne verticale droite (y=6 à 7, x=11)
        for y in range(6, 8):
            grid[y][11] = 'tree'
        
        # Ligne horizontale haut (y=2, x=6 à 8)
        for x in range(6, 9):
            grid[2][x] = 'tree'
        
        # Arbres isolés
        grid[3][7] = 'tree'
        grid[8][8] = 'tree'
        grid[9][7] = 'tree'
        grid[9][8] = 'tree'
        grid[9][9] = 'tree'
        grid[8][4] = 'tree'
        grid[9][4] = 'tree'
        grid[10][4] = 'tree'
        grid[1][11] = 'tree'
        grid[2][11] = 'tree'
        grid[3][11] = 'tree'
        grid[2][4] = 'tree'
        grid[10][11] = 'tree'
        grid[2][13] = 'tree'
        grid[2][14] = 'tree'
        grid[9][1] = 'tree'
        grid[9][2] = 'tree'
        grid[5][1] = 'tree'
        grid[6][1] = 'tree'
        grid[7][1] = 'tree'
        grid[4][14] = 'tree'
        grid[5][14] = 'tree'
        grid[6][14] = 'tree'
        
        grid[5][5] = 'dirt'
        grid[5][6] = 'dirt'
        grid[6][9] = 'dirt'
        grid[6][10] = 'dirt'
        grid[7][10] = 'dirt'
        grid[4][5] = 'dirt'

        
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