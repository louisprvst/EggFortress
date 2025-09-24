import random
import os
import pygame

class Map:
    """
    Gestionnaire de carte procédurale avec terrain et décorations
    
    Génère automatiquement une carte naturelle composée :
    - D'un terrain de base (herbe/terre)  
    - De décorations par-dessus (arbres, buissons, fleurs)
    - De chemins connectés pour la navigation
    """
    
    # Configuration des assets et leurs tailles
    ASSET_CONFIG = [
        {'file': 'bush.png', 'scale': 1.0},
        {'file': 'dirt.png', 'scale': 1.0}, 
        {'file': 'flower.png', 'scale': 0.5},
        {'file': 'flower_2.png', 'scale': 0.5},
        {'file': 'flower_3.png', 'scale': 0.5},
        {'file': 'flower_4.png', 'scale': 0.5},
        {'file': 'grass.png', 'scale': 1.0},
        {'file': 'tree.png', 'scale': 2.2},
    ]
    
    # Types de fleurs disponibles
    FLOWER_TYPES = ['flower', 'flower_2', 'flower_3', 'flower_4']
    
    # Décorations solides pour les collisions
    SOLID_DECORATIONS = ['tree', 'bush']
    
    def __init__(self, screen_width, screen_height, tile_size=32, assets_path="assets/images/Map/"):
        """
        Initialise une nouvelle carte
        
        Args:
            screen_width: Largeur de l'écran en pixels
            screen_height: Hauteur de l'écran en pixels  
            tile_size: Taille d'une tuile en pixels (défaut: 32)
            assets_path: Chemin vers les ressources graphiques
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size
        self.assets_path = assets_path
        
        # Calculer la grille pour couvrir tout l'écran + marge
        self.grid_width = (screen_width // tile_size) + 4
        self.grid_height = (screen_height // tile_size) + 4
        
        # Assets chargés en mémoire
        self.assets = {}
        
        # Initialisation
        self._load_assets()
        self.terrain_grid, self.decoration_grid = self._generate_map()
        
    def _load_assets(self):
        """Charge et redimensionne tous les assets graphiques"""
        loaded_count = 0
        
        for config in self.ASSET_CONFIG:
            asset_path = os.path.join(self.assets_path, config['file'])
            
            if not os.path.exists(asset_path):
                print(f"⚠️ Asset manquant: {config['file']}")
                continue
                
            try:
                # Charger et redimensionner l'image
                original_img = pygame.image.load(asset_path).convert_alpha()
                new_size = int(self.tile_size * config['scale'])
                scaled_img = pygame.transform.scale(original_img, (new_size, new_size))
                
                # Stocker sans l'extension .png
                asset_name = config['file'].replace('.png', '')
                self.assets[asset_name] = scaled_img
                loaded_count += 1
                
            except pygame.error as e:
                print(f"⚠️ Erreur lors du chargement de {config['file']}: {e}")
        
        print(f"✅ {loaded_count}/{len(self.ASSET_CONFIG)} assets chargés")
    
    def _generate_map(self):
        """
        Génère une carte naturelle avec terrain et décorations
        
        Returns:
            tuple: (terrain_grid, decoration_grid)
        """
        # Initialiser les grilles vides
        terrain_grid = self._create_empty_grid()
        decoration_grid = self._create_empty_grid()
        
        # Générer le terrain de base avec bruit procédural
        self._generate_base_terrain(terrain_grid)
        
        # Créer des chemins connectés
        self._create_connected_paths(terrain_grid)
        
        # Ajouter végétation et décorations
        self._add_decorations(terrain_grid, decoration_grid)
        
        return terrain_grid, decoration_grid
    
    def _create_empty_grid(self):
        """Crée une grille vide de la taille appropriée"""
        return [[None for _ in range(self.grid_width)] 
                for _ in range(self.grid_height)]
    
    def _generate_base_terrain(self, terrain_grid):
        """Génère le terrain de base (herbe/terre) avec bruit procédural"""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                terrain_grid[y][x] = self._get_terrain_type(x, y)
    
    def _get_terrain_type(self, x, y):
        """
        Détermine le type de terrain pour une position donnée
        
        Utilise un bruit multi-octave pour des formes organiques
        """
        # Paramètres de bruit pour variation naturelle
        scale = 0.08
        seed_x, seed_y = x * scale, y * scale
        
        # Combiner plusieurs couches de bruit
        noise_layers = [
            random.Random(int((seed_x + seed_y) * 1000)).random() * 0.5,
            random.Random(int(seed_x * 1500)).random() * 0.3,
            random.Random(int(seed_y * 800)).random() * 0.2
        ]
        
        combined_noise = sum(noise_layers)
        
        # 60% herbe, 40% terre pour un équilibre naturel
        return 'grass' if combined_noise > 0.4 else 'dirt'
    
    def _add_decorations(self, terrain_grid, decoration_grid):
        """Ajoute la végétation et les décorations sur le terrain"""
        for y in range(len(terrain_grid)):
            for x in range(len(terrain_grid[y])):
                terrain_type = terrain_grid[y][x]
                
                if terrain_type == 'grass':
                    decoration_grid[y][x] = self._get_grass_decoration()
                elif terrain_type == 'dirt':
                    decoration_grid[y][x] = self._get_dirt_decoration()
    
    def _get_grass_decoration(self):
        """Détermine la décoration pour une case d'herbe (20% de chance)"""
        if random.random() >= 0.2:
            return None
            
        decoration_roll = random.random()
        
        if decoration_roll < 0.25:      # 25% arbres
            return 'tree'
        elif decoration_roll < 0.45:    # 20% buissons  
            return 'bush'
        else:                           # 55% fleurs variées
            return random.choice(self.FLOWER_TYPES)
    
    def _get_dirt_decoration(self):
        """Détermine la décoration pour une case de terre (8% de chance)"""
        if random.random() >= 0.08:
            return None
            
        # Seules certaines plantes poussent sur terre
        return random.choice(['flower_3', 'flower_4', 'bush'])
    
    def _create_connected_paths(self, terrain_grid):
        """Crée un réseau de chemins connectés à travers la carte"""
        # Générer des points d'intérêt à relier
        waypoints = self._generate_waypoints()
        
        # Connecter les waypoints en boucle
        self._connect_waypoints(terrain_grid, waypoints)
        
        # Ajouter des chemins secondaires pour plus de variété
        self._add_secondary_paths(terrain_grid)
    
    def _generate_waypoints(self):
        """Génère 4-7 points d'intérêt aléatoires sur la carte"""
        num_waypoints = random.randint(4, 7)
        waypoints = []
        
        for _ in range(num_waypoints):
            # Éviter les bords pour les waypoints
            x = random.randint(1, self.grid_width - 2)
            y = random.randint(1, self.grid_height - 2)
            waypoints.append((x, y))
            
        return waypoints
    
    def _connect_waypoints(self, terrain_grid, waypoints):
        """Connecte tous les waypoints en formant une boucle"""
        for i in range(len(waypoints)):
            start = waypoints[i]
            end = waypoints[(i + 1) % len(waypoints)]  # Boucle vers le premier
            self._create_path(terrain_grid, start, end)
    
    def _add_secondary_paths(self, terrain_grid):
        """Ajoute 2-3 chemins secondaires aléatoires"""
        num_paths = random.randint(2, 3)
        
        for _ in range(num_paths):
            start_x = random.randint(0, self.grid_width - 1)
            start_y = random.randint(0, self.grid_height - 1)
            self._create_random_path(terrain_grid, start_x, start_y)
    
    def _create_path(self, terrain_grid, start_pos, end_pos):
        """Crée un chemin entre deux points avec algorithme de Bresenham"""
        current_x, current_y = start_pos
        target_x, target_y = end_pos
        
        while current_x != target_x or current_y != target_y:
            # Placer de la terre à la position actuelle
            if self._is_valid_position(current_x, current_y):
                terrain_grid[current_y][current_x] = 'dirt'
                self._widen_path(terrain_grid, current_x, current_y)
            
            # Se rapprocher de la cible
            current_x = self._move_toward_target(current_x, target_x)
            current_y = self._move_toward_target(current_y, target_y)
            
            # Variation naturelle occasionnelle (20% de chance)
            if random.random() < 0.2:
                current_x, current_y = self._add_path_variation(current_x, current_y)
    
    def _move_toward_target(self, current, target):
        """Déplace une coordonnée vers sa cible"""
        if current < target:
            return current + 1
        elif current > target:
            return current - 1
        return current
    
    def _widen_path(self, terrain_grid, x, y):
        """Élargit légèrement un chemin (30% de chance par case adjacente)"""
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_x, adj_y = x + dx, y + dy
            if (self._is_valid_position(adj_x, adj_y) and random.random() < 0.3):
                terrain_grid[adj_y][adj_x] = 'dirt'
    
    def _add_path_variation(self, x, y):
        """Ajoute une variation naturelle à un chemin"""
        x += random.choice([-1, 0, 1])
        y += random.choice([-1, 0, 1])
        
        # Rester dans les limites
        x = max(0, min(self.grid_width - 1, x))
        y = max(0, min(self.grid_height - 1, y))
        
        return x, y
    
    def _is_valid_position(self, x, y):
        """Vérifie si une position est dans les limites de la grille"""
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height
    
    def _create_random_path(self, terrain_grid, start_x, start_y):
        """Crée un chemin aléatoire dans une direction générale"""
        current_x, current_y = start_x, start_y
        path_length = random.randint(8, 15)
        
        # Choisir une direction principale
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        
        for _ in range(path_length):
            if self._is_valid_position(current_x, current_y):
                terrain_grid[current_y][current_x] = 'dirt'
            
            # 70% de chance de suivre la direction principale
            if random.random() < 0.7:
                current_x += direction[0] 
                current_y += direction[1]
            else:
                # 30% de chance de dévier
                current_x += random.choice([-1, 0, 1])
                current_y += random.choice([-1, 0, 1])
            
            # Garder dans les limites
            current_x = max(0, min(self.grid_width - 1, current_x))
            current_y = max(0, min(self.grid_height - 1, current_y))
    

    
    def draw(self, screen, camera_x=0, camera_y=0):
        """
        Dessine la carte avec optimisation du culling
        
        Args:
            screen: Surface pygame pour le rendu
            camera_x, camera_y: Position de la caméra
        """
        # Calculer la zone visible (culling)
        visible_area = self._get_visible_area(camera_x, camera_y)
        
        # Rendu en deux passes pour la profondeur
        self._draw_terrain(screen, camera_x, camera_y, visible_area)
        self._draw_decorations(screen, camera_x, camera_y, visible_area)
    
    def _get_visible_area(self, camera_x, camera_y):
        """Calcule la zone visible pour l'optimisation du rendu"""
        start_x = max(0, camera_x // self.tile_size)
        end_x = min(self.grid_width, (camera_x + self.screen_width) // self.tile_size + 2)
        start_y = max(0, camera_y // self.tile_size)  
        end_y = min(self.grid_height, (camera_y + self.screen_height) // self.tile_size + 2)
        
        return {'start_x': start_x, 'end_x': end_x, 'start_y': start_y, 'end_y': end_y}
    
    def _draw_terrain(self, screen, camera_x, camera_y, visible_area):
        """Première passe : rendu du terrain de base"""
        for y in range(visible_area['start_y'], visible_area['end_y']):
            for x in range(visible_area['start_x'], visible_area['end_x']):
                if not self._is_valid_grid_position(x, y):
                    continue
                    
                terrain_type = self.terrain_grid[y][x]
                screen_pos = (x * self.tile_size - camera_x, y * self.tile_size - camera_y)
                
                self._draw_tile(screen, terrain_type, screen_pos)
    
    def _draw_decorations(self, screen, camera_x, camera_y, visible_area):
        """Deuxième passe : rendu des décorations"""
        for y in range(visible_area['start_y'], visible_area['end_y']):
            for x in range(visible_area['start_x'], visible_area['end_x']):
                if not self._is_valid_grid_position(x, y):
                    continue
                    
                decoration = self.decoration_grid[y][x]
                if decoration is None:
                    continue
                
                base_pos = (x * self.tile_size - camera_x, y * self.tile_size - camera_y)
                self._draw_decoration(screen, decoration, base_pos)
    
    def _draw_tile(self, screen, tile_type, screen_pos):
        """Dessine une tuile de terrain"""
        tile_image = self.assets.get(tile_type)
        
        if tile_image:
            screen.blit(tile_image, screen_pos)
        else:
            # Fallback coloré si asset manquant
            color = self._get_fallback_color(tile_type)
            rect = (*screen_pos, self.tile_size, self.tile_size)
            pygame.draw.rect(screen, color, rect)
    
    def _draw_decoration(self, screen, decoration_type, base_pos):
        """Dessine une décoration avec positionnement correct"""
        decoration_img = self.assets.get(decoration_type)
        
        if decoration_img:
            # Calculer la position centrée
            img_size = decoration_img.get_size()
            offset_x = (self.tile_size - img_size[0]) // 2
            offset_y = (self.tile_size - img_size[1]) // 2
            
            # Ancrer les arbres au sol
            if decoration_type == 'tree':
                offset_y = self.tile_size - int(img_size[1] * 0.85)
            
            final_pos = (base_pos[0] + offset_x, base_pos[1] + offset_y)
            screen.blit(decoration_img, final_pos)
        else:
            # Fallback coloré
            color = self._get_fallback_color(decoration_type)
            rect = (*base_pos, self.tile_size, self.tile_size)
            pygame.draw.rect(screen, color, rect)
    
    def _is_valid_grid_position(self, x, y):
        """Vérifie si une position de grille est valide"""
        return (0 <= y < len(self.terrain_grid) and 
                0 <= x < len(self.terrain_grid[y]))
    
    def _get_fallback_color(self, tile_type):
        """Couleurs de secours si les assets manquent"""
        fallback_colors = {
            'grass': (34, 139, 34),      # Vert forêt
            'dirt': (139, 69, 19),       # Brun terre  
            'tree': (0, 100, 0),         # Vert foncé
            'bush': (107, 142, 35),      # Vert olive
            'flower': (255, 192, 203),   # Rose
            'flower_2': (255, 255, 0),   # Jaune
            'flower_3': (255, 165, 0),   # Orange  
            'flower_4': (128, 0, 128),   # Violet
        }
        return fallback_colors.get(tile_type, (128, 128, 128))
    
    # ===== API PUBLIQUE =====
    
    def get_total_width(self):
        """Largeur totale de la carte en pixels"""
        return self.grid_width * self.tile_size
    
    def get_total_height(self):
        """Hauteur totale de la carte en pixels"""
        return self.grid_height * self.tile_size
    
    def is_solid(self, pixel_x, pixel_y):
        """
        Teste si une position en pixels contient un obstacle
        
        Args:
            pixel_x, pixel_y: Position en coordonnées écran
            
        Returns:
            bool: True si la position est bloquée par un obstacle
        """
        # Convertir les pixels en coordonnées de grille
        grid_x = pixel_x // self.tile_size
        grid_y = pixel_y // self.tile_size
        
        # Vérifier les limites
        if not (0 <= grid_y < len(self.decoration_grid) and 
                0 <= grid_x < len(self.decoration_grid[grid_y])):
            return False
        
        # Tester si la décoration est solide
        decoration = self.decoration_grid[grid_y][grid_x]
        return decoration in self.SOLID_DECORATIONS
    
    def regenerate(self):
        """Génère une nouvelle carte aléatoire"""
        self.terrain_grid, self.decoration_grid = self._generate_map()
        print("🔄 Nouvelle carte générée!")