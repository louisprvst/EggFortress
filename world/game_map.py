import pygame
import os
import sys
from game_manager import GameManager

class GameMap:
    def __init__(self, ecran, largeur_grille=15, hauteur_grille=10):
        self.ecran = ecran
        self.largeur_ecran = ecran.get_width()
        self.hauteur_ecran = ecran.get_height()
        
        # Dimensions de la grille
        self.largeur_grille = largeur_grille
        self.hauteur_grille = hauteur_grille
        
        # Calcul des dimensions des cases pour s'adapter à l'écran
        self.taille_case_x = (self.largeur_ecran - 200) // largeur_grille  # Marges de 100px de chaque côté
        self.taille_case_y = (self.hauteur_ecran - 200) // hauteur_grille  # Marges de 100px en haut et en bas
        
        # Calcul de la position de départ pour centrer la grille
        self.offset_x = (self.largeur_ecran - (largeur_grille * self.taille_case_x)) // 2
        self.offset_y = (self.hauteur_ecran - (hauteur_grille * self.taille_case_y)) // 2
        
        # Grille pour stocker le contenu de chaque case
        self.grille = [[None for _ in range(largeur_grille)] for _ in range(hauteur_grille)]
        
        # Grille pour les cases bloquées (True = bloquée, False = libre)
        self.cases_bloquees = [[False for _ in range(largeur_grille)] for _ in range(hauteur_grille)]
        
        # Case sélectionnée
        self.case_selectionnee = None
        self.case_survol = None
        
        # Couleurs
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS = (128, 128, 128)
        self.GRIS_CLAIR = (200, 200, 200)
        self.BLEU = (100, 150, 255)
        self.VERT = (100, 255, 100)
        self.ROUGE = (255, 100, 100)
        self.JAUNE = (255, 255, 100)
        
        # États de jeu
        self.mode_placement = None  # 'dinosaure', 'piege', 'oeuf', etc.
        self.running = True
        self.horloge = pygame.time.Clock()
        
        # Gestionnaire de jeu pour le tour par tour
        self.game_manager = GameManager()
        
        # Charger les assets
        self._charger_assets()
        
        # Interface utilisateur
        self._creer_interface()
        
        # Créer quelques cases bloquées par défaut (exemple)
        self._creer_cases_bloquees_exemple()
    
    def _charger_assets(self):
        """Charge les images nécessaires"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, "..", "assets", "images")
        
        try:
            # Charger les images des dinosaures
            dino_dir = os.path.join(assets_dir, "Dinos")
            self.dino_images = {
                'diplodocus_bleu': pygame.image.load(os.path.join(dino_dir, "Dino1_Blue.png")),
                'parasaure_bleu': pygame.image.load(os.path.join(dino_dir, "Dino2_Blue.png")),
                'trex_bleu': pygame.image.load(os.path.join(dino_dir, "Dino3_Blue.png")),
                'diplodocus_rouge': pygame.image.load(os.path.join(dino_dir, "Dino1_Red.png")),
                'parasaure_rouge': pygame.image.load(os.path.join(dino_dir, "Dino2_Red.png")),
                'trex_rouge': pygame.image.load(os.path.join(dino_dir, "Dino3_Red.png"))
            }
            
            # Redimensionner les images pour s'adapter aux cases
            for key in self.dino_images:
                self.dino_images[key] = pygame.transform.scale(
                    self.dino_images[key], 
                    (self.taille_case_x - 10, self.taille_case_y - 10)
                )
            
            # Charger les images des œufs
            egg_dir = os.path.join(assets_dir, "Eggs")
            self.egg_images = {
                'blue': pygame.image.load(os.path.join(egg_dir, "blue_egg.png")),
                'red': pygame.image.load(os.path.join(egg_dir, "red_egg.png"))
            }
            
            for key in self.egg_images:
                self.egg_images[key] = pygame.transform.scale(
                    self.egg_images[key], 
                    (self.taille_case_x - 10, self.taille_case_y - 10)
                )
            
            # Charger l'image du piège
            trap_dir = os.path.join(assets_dir, "Traps")
            self.trap_image = pygame.image.load(os.path.join(trap_dir, "trap.png"))
            self.trap_image = pygame.transform.scale(
                self.trap_image, 
                (self.taille_case_x - 10, self.taille_case_y - 10)
            )
            
        except pygame.error as e:
            print(f"Erreur lors du chargement des assets: {e}")
            # Images de fallback (rectangles colorés)
            self.dino_images = {
                'diplodocus_bleu': None,
                'parasaure_bleu': None,
                'trex_bleu': None,
                'diplodocus_rouge': None,
                'parasaure_rouge': None,
                'trex_rouge': None
            }
            self.egg_images = {'blue': None, 'red': None}
            self.trap_image = None
    
    def _creer_interface(self):
        """Crée les boutons d'interface"""
        self.font = pygame.font.Font(None, 24)
        self.font_titre = pygame.font.Font(None, 32)
        
        # Boutons de placement
        bouton_width = 120
        bouton_height = 40
        start_y = 50
        
        self.boutons = {
            'diplodocus_bleu': pygame.Rect(20, start_y, bouton_width, bouton_height),
            'parasaure_bleu': pygame.Rect(20, start_y + 50, bouton_width, bouton_height),
            'trex_bleu': pygame.Rect(20, start_y + 100, bouton_width, bouton_height),
            'diplodocus_rouge': pygame.Rect(20, start_y + 150, bouton_width, bouton_height),
            'parasaure_rouge': pygame.Rect(20, start_y + 200, bouton_width, bouton_height),
            'trex_rouge': pygame.Rect(20, start_y + 250, bouton_width, bouton_height),
            'oeuf_bleu': pygame.Rect(20, start_y + 300, bouton_width, bouton_height),
            'oeuf_rouge': pygame.Rect(20, start_y + 350, bouton_width, bouton_height),
            'piege': pygame.Rect(20, start_y + 400, bouton_width, bouton_height),
            'bloquer': pygame.Rect(20, start_y + 450, bouton_width, bouton_height),
            'effacer': pygame.Rect(20, start_y + 500, bouton_width, bouton_height),
            'passer_tour': pygame.Rect(20, start_y + 550, bouton_width, bouton_height),
            'reset': pygame.Rect(20, start_y + 600, bouton_width, bouton_height),
            'retour': pygame.Rect(20, self.hauteur_ecran - 80, bouton_width, bouton_height)
        }
    
    def obtenir_case_sous_souris(self, pos_souris):
        """Retourne les coordonnées de la case sous la souris"""
        x, y = pos_souris
        
        # Vérifier si la souris est dans la zone de la grille
        if (self.offset_x <= x <= self.offset_x + self.largeur_grille * self.taille_case_x and
            self.offset_y <= y <= self.offset_y + self.hauteur_grille * self.taille_case_y):
            
            case_x = (x - self.offset_x) // self.taille_case_x
            case_y = (y - self.offset_y) // self.taille_case_y
            
            return (case_x, case_y)
        
        return None
    
    def _creer_cases_bloquees_exemple(self):
        """Crée quelques cases bloquées par défaut pour l'exemple"""
        # Exemple : bloquer quelques cases au milieu de la map
        centre_x = self.largeur_grille // 2
        centre_y = self.hauteur_grille // 2
        
        # Créer un petit obstacle au centre
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = centre_x + dx
                y = centre_y + dy
                if 0 <= x < self.largeur_grille and 0 <= y < self.hauteur_grille:
                    self.cases_bloquees[y][x] = True
        
        # Quelques cases bloquées aléatoires sur les bords
        import random
        for _ in range(8):
            x = random.randint(0, self.largeur_grille - 1)
            y = random.randint(0, self.hauteur_grille - 1)
            # Ne pas bloquer les coins pour laisser de l'espace de jeu
            if not ((x < 2 and y < 2) or (x >= self.largeur_grille - 2 and y < 2) or 
                    (x < 2 and y >= self.hauteur_grille - 2) or 
                    (x >= self.largeur_grille - 2 and y >= self.hauteur_grille - 2)):
                self.cases_bloquees[y][x] = True
    
    def basculer_case_bloquee(self, case_x, case_y):
        """Bascule l'état bloqué/libre d'une case"""
        if 0 <= case_x < self.largeur_grille and 0 <= case_y < self.hauteur_grille:
            self.cases_bloquees[case_y][case_x] = not self.cases_bloquees[case_y][case_x]
            # Si on bloque une case qui contient quelque chose, l'effacer
            if self.cases_bloquees[case_y][case_x] and self.grille[case_y][case_x]:
                self.grille[case_y][case_x] = None
            print(f"Case ({case_x}, {case_y}) {'bloquée' if self.cases_bloquees[case_y][case_x] else 'débloquée'}")
    
    def est_case_bloquee(self, case_x, case_y):
        """Vérifie si une case est bloquée"""
        if 0 <= case_x < self.largeur_grille and 0 <= case_y < self.hauteur_grille:
            return self.cases_bloquees[case_y][case_x]
        return True  # Les cases hors limites sont considérées comme bloquées
    
    def placer_element(self, case_x, case_y, type_element):
        """Place un élément dans une case de la grille"""
        if 0 <= case_x < self.largeur_grille and 0 <= case_y < self.hauteur_grille:
            # Vérifier si la case est bloquée
            if self.est_case_bloquee(case_x, case_y):
                print(f"Impossible de placer '{type_element}' en case ({case_x}, {case_y}) - Case bloquée!")
                return False
            
            # Vérifier si le joueur peut placer cet élément
            if not self.game_manager.peut_placer_element(type_element):
                joueur = self.game_manager.get_joueur_actuel()
                print(f"Impossible de placer '{type_element}' - {joueur['nom']} ne peut pas placer cet élément maintenant!")
                return False
            
            # Placer l'élément
            self.grille[case_y][case_x] = type_element
            
            # Enregistrer dans le gestionnaire de jeu
            if self.game_manager.placer_element(type_element):
                print(f"Élément '{type_element}' placé en case ({case_x}, {case_y}) par {self.game_manager.get_joueur_actuel()['nom']}")
                
                # Passer automatiquement au suivant après placement
                self.game_manager.passer_au_suivant()
                return True
            else:
                # Annuler le placement si le gestionnaire refuse
                self.grille[case_y][case_x] = None
                return False
        return False
    
    def effacer_element(self, case_x, case_y):
        """Efface l'élément d'une case"""
        if 0 <= case_x < self.largeur_grille and 0 <= case_y < self.hauteur_grille:
            ancien_element = self.grille[case_y][case_x]
            self.grille[case_y][case_x] = None
            if ancien_element:
                print(f"Élément '{ancien_element}' effacé de la case ({case_x}, {case_y})")
    
    def gerer_evenements(self):
        """Gère les événements de la map"""
        pos_souris = pygame.mouse.get_pos()
        self.case_survol = self.obtenir_case_sous_souris(pos_souris)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    # Vérifier les boutons
                    for nom_bouton, rect_bouton in self.boutons.items():
                        if rect_bouton.collidepoint(pos_souris):
                            if nom_bouton == 'retour':
                                return "menu"
                            elif nom_bouton == 'effacer':
                                self.mode_placement = 'effacer'
                            elif nom_bouton == 'bloquer':
                                self.mode_placement = 'bloquer'
                            elif nom_bouton == 'passer_tour':
                                self.game_manager.passer_au_suivant()
                                self.mode_placement = None
                                print(f"Tour passé - C'est maintenant à {self.game_manager.get_joueur_actuel()['nom']}")
                            elif nom_bouton == 'reset':
                                self.game_manager.reset()
                                # Effacer toute la grille sauf les cases bloquées
                                for y in range(self.hauteur_grille):
                                    for x in range(self.largeur_grille):
                                        if not self.est_case_bloquee(x, y):
                                            self.grille[y][x] = None
                                self.mode_placement = None
                                print("Jeu remis à zéro!")
                            else:
                                # Vérifier si l'élément est autorisé pour le joueur actuel
                                if self.game_manager.peut_placer_element(nom_bouton):
                                    self.mode_placement = nom_bouton
                                else:
                                    joueur = self.game_manager.get_joueur_actuel()
                                    elements_autorises = self.game_manager.get_elements_autorises()
                                    print(f"{joueur['nom']} ne peut placer que: {elements_autorises}")
                                    self.mode_placement = None
                            return None
                    
                    # Clic sur la grille
                    case = self.obtenir_case_sous_souris(pos_souris)
                    if case:
                        case_x, case_y = case
                        self.case_selectionnee = case
                        
                        if self.mode_placement == 'effacer':
                            self.effacer_element(case_x, case_y)
                        elif self.mode_placement == 'bloquer':
                            self.basculer_case_bloquee(case_x, case_y)
                        elif self.mode_placement:
                            self.placer_element(case_x, case_y, self.mode_placement)
        
        return None
    
    def _dessiner_bouton(self, rect, texte, est_actif=False, est_autorise=True):
        """Dessine un bouton"""
        pos_souris = pygame.mouse.get_pos()
        
        if not est_autorise:
            couleur_fond = self.GRIS
            couleur_texte = self.NOIR
        elif est_actif:
            couleur_fond = self.VERT
            couleur_texte = self.NOIR
        elif rect.collidepoint(pos_souris):
            couleur_fond = self.GRIS_CLAIR
            couleur_texte = self.NOIR
        else:
            couleur_fond = self.BLANC
            couleur_texte = self.NOIR
        
        pygame.draw.rect(self.ecran, couleur_fond, rect)
        pygame.draw.rect(self.ecran, self.NOIR, rect, 2)
        
        texte_surface = self.font.render(texte, True, couleur_texte)
        texte_x = rect.x + (rect.width - texte_surface.get_width()) // 2
        texte_y = rect.y + (rect.height - texte_surface.get_height()) // 2
        self.ecran.blit(texte_surface, (texte_x, texte_y))
    
    def _dessiner_case(self, case_x, case_y):
        """Dessine une case de la grille"""
        x = self.offset_x + case_x * self.taille_case_x
        y = self.offset_y + case_y * self.taille_case_y
        
        rect_case = pygame.Rect(x, y, self.taille_case_x, self.taille_case_y)
        
        # Couleur de fond de la case
        if self.est_case_bloquee(case_x, case_y):
            couleur_fond = self.NOIR
        elif self.case_survol == (case_x, case_y):
            couleur_fond = self.JAUNE
        elif self.case_selectionnee == (case_x, case_y):
            couleur_fond = self.BLEU
        else:
            couleur_fond = self.BLANC
        
        pygame.draw.rect(self.ecran, couleur_fond, rect_case)
        pygame.draw.rect(self.ecran, self.GRIS if self.est_case_bloquee(case_x, case_y) else self.NOIR, rect_case, 1)
        
        # Dessiner le contenu de la case seulement si elle n'est pas bloquée
        if not self.est_case_bloquee(case_x, case_y):
            contenu = self.grille[case_y][case_x]
            if contenu:
                self._dessiner_contenu_case(x + 5, y + 5, contenu)
    
    def _dessiner_contenu_case(self, x, y, contenu):
        """Dessine le contenu d'une case"""
        if contenu in ['diplodocus_bleu', 'parasaure_bleu', 'trex_bleu', 
                      'diplodocus_rouge', 'parasaure_rouge', 'trex_rouge'] and contenu in self.dino_images:
            if self.dino_images[contenu]:
                self.ecran.blit(self.dino_images[contenu], (x, y))
            else:
                # Fallback: rectangle coloré selon la couleur du dinosaure
                if 'bleu' in contenu:
                    if 'diplodocus' in contenu:
                        couleur = self.BLEU
                    elif 'parasaure' in contenu:
                        couleur = (0, 100, 255)  # Bleu plus foncé
                    else:  # trex
                        couleur = (0, 0, 200)  # Bleu très foncé
                else:  # rouge
                    if 'diplodocus' in contenu:
                        couleur = self.ROUGE
                    elif 'parasaure' in contenu:
                        couleur = (255, 100, 0)  # Rouge-orange
                    else:  # trex
                        couleur = (200, 0, 0)  # Rouge foncé
                pygame.draw.rect(self.ecran, couleur, pygame.Rect(x, y, self.taille_case_x - 10, self.taille_case_y - 10))
        
        elif contenu in ['oeuf_bleu', 'oeuf_rouge']:
            egg_type = 'blue' if 'bleu' in contenu else 'red'
            if self.egg_images[egg_type]:
                self.ecran.blit(self.egg_images[egg_type], (x, y))
            else:
                couleur = self.BLEU if 'bleu' in contenu else self.ROUGE
                pygame.draw.circle(self.ecran, couleur, (x + self.taille_case_x//4, y + self.taille_case_y//4), min(self.taille_case_x, self.taille_case_y)//4)
        
        elif contenu == 'piege':
            if self.trap_image:
                self.ecran.blit(self.trap_image, (x, y))
            else:
                pygame.draw.polygon(self.ecran, self.ROUGE, [
                    (x + self.taille_case_x//4, y + self.taille_case_y//4),
                    (x + 3*self.taille_case_x//4, y + self.taille_case_y//4),
                    (x + self.taille_case_x//2, y + 3*self.taille_case_y//4)
                ])
    
    def dessiner(self):
        """Dessine la map complète"""
        # Fond
        self.ecran.fill(self.GRIS)
        
        # Titre
        titre = self.font_titre.render("Egg Fortress - Éditeur de Map", True, self.BLANC)
        self.ecran.blit(titre, (self.largeur_ecran//2 - titre.get_width()//2, 10))
        
        # Grille
        for case_y in range(self.hauteur_grille):
            for case_x in range(self.largeur_grille):
                self._dessiner_case(case_x, case_y)
        
        # Interface utilisateur
        # Boutons de placement avec vérification des autorisations
        elements_autorises = self.game_manager.get_elements_autorises()
        
        # Dinosaures bleus
        self._dessiner_bouton(self.boutons['diplodocus_bleu'], "Diplo Bleu", 
                            self.mode_placement == 'diplodocus_bleu', 
                            'diplodocus_bleu' in elements_autorises)
        self._dessiner_bouton(self.boutons['parasaure_bleu'], "Para Bleu", 
                            self.mode_placement == 'parasaure_bleu', 
                            'parasaure_bleu' in elements_autorises)
        self._dessiner_bouton(self.boutons['trex_bleu'], "T-Rex Bleu", 
                            self.mode_placement == 'trex_bleu', 
                            'trex_bleu' in elements_autorises)
        
        # Dinosaures rouges
        self._dessiner_bouton(self.boutons['diplodocus_rouge'], "Diplo Rouge", 
                            self.mode_placement == 'diplodocus_rouge', 
                            'diplodocus_rouge' in elements_autorises)
        self._dessiner_bouton(self.boutons['parasaure_rouge'], "Para Rouge", 
                            self.mode_placement == 'parasaure_rouge', 
                            'parasaure_rouge' in elements_autorises)
        self._dessiner_bouton(self.boutons['trex_rouge'], "T-Rex Rouge", 
                            self.mode_placement == 'trex_rouge', 
                            'trex_rouge' in elements_autorises)
        
        # Œufs
        self._dessiner_bouton(self.boutons['oeuf_bleu'], "Œuf Bleu", 
                            self.mode_placement == 'oeuf_bleu', 
                            'oeuf_bleu' in elements_autorises)
        self._dessiner_bouton(self.boutons['oeuf_rouge'], "Œuf Rouge", 
                            self.mode_placement == 'oeuf_rouge', 
                            'oeuf_rouge' in elements_autorises)
        
        # Autres éléments
        self._dessiner_bouton(self.boutons['piege'], "Piège", 
                            self.mode_placement == 'piege', 
                            'piege' in elements_autorises)
        
        # Boutons utilitaires (toujours disponibles)
        self._dessiner_bouton(self.boutons['bloquer'], "Bloquer", self.mode_placement == 'bloquer')
        self._dessiner_bouton(self.boutons['effacer'], "Effacer", self.mode_placement == 'effacer')
        self._dessiner_bouton(self.boutons['passer_tour'], "Passer Tour", False)
        self._dessiner_bouton(self.boutons['reset'], "Reset", False)
        self._dessiner_bouton(self.boutons['retour'], "Retour", False)
        
        # Informations de jeu
        info_y = 50
        
        # Statut du jeu (qui doit jouer)
        status_text = self.game_manager.get_status_text()
        status_surface = self.font_titre.render("STATUT", True, self.BLANC)
        self.ecran.blit(status_surface, (self.largeur_ecran - 300, info_y))
        
        # Couleur du joueur actuel
        joueur_actuel = self.game_manager.get_joueur_actuel()
        couleur_joueur = self.BLEU if joueur_actuel['couleur'] == 'bleu' else self.ROUGE
        
        status_lines = status_text.split(' - ')
        for i, line in enumerate(status_lines):
            line_surface = self.font.render(line, True, couleur_joueur if i == 1 else self.BLANC)
            self.ecran.blit(line_surface, (self.largeur_ecran - 300, info_y + 40 + i * 25))
        
        # Éléments autorisés
        elements_autorises = self.game_manager.get_elements_autorises()
        if elements_autorises:
            autorise_text = f"Peut placer: {', '.join(elements_autorises)}"
        else:
            autorise_text = "Aucun élément autorisé - Passez le tour"
        autorise_surface = self.font.render(autorise_text, True, self.JAUNE)
        self.ecran.blit(autorise_surface, (self.largeur_ecran - 300, info_y + 100))
        
        # Compteurs des joueurs
        compteurs = self.game_manager.get_compteurs_text()
        for i, compteur in enumerate(compteurs):
            couleur = self.BLEU if i == 0 else self.ROUGE
            compteur_surface = self.font.render(compteur, True, couleur)
            self.ecran.blit(compteur_surface, (self.largeur_ecran - 400, info_y + 140 + i * 25))
        
        # Informations de la case survolée
        if self.case_survol:
            info_text = f"Case: {self.case_survol}"
            contenu = self.grille[self.case_survol[1]][self.case_survol[0]]
            if self.est_case_bloquee(self.case_survol[0], self.case_survol[1]):
                info_text += " - BLOQUÉE"
            elif contenu:
                info_text += f" - {contenu}"
            info_surface = self.font.render(info_text, True, self.BLANC)
            self.ecran.blit(info_surface, (self.largeur_ecran - 250, info_y + 200))
        
        if self.mode_placement:
            mode_text = f"Mode: {self.mode_placement}"
            mode_surface = self.font.render(mode_text, True, self.BLANC)
            self.ecran.blit(mode_surface, (self.largeur_ecran - 250, info_y + 230))
        
        # Instructions
        instructions = [
            "TOUR PAR TOUR:",
            "1. Chaque joueur place son œuf",
            "2. Alternance pour les dinosaures",
            "Boutons grisés = non autorisés",
            "'Passer Tour' si coincé",
            "ESC ou Retour pour le menu"
        ]
        
        for i, instruction in enumerate(instructions):
            couleur = self.JAUNE if i == 0 else self.BLANC
            inst_surface = self.font.render(instruction, True, couleur)
            self.ecran.blit(inst_surface, (self.largeur_ecran - 300, self.hauteur_ecran - 180 + i * 25))
        
        pygame.display.flip()
    
    def executer(self):
        """Boucle principale de la map"""
        while self.running:
            action = self.gerer_evenements()
            
            if action == "menu":
                return "menu"
            elif action == "quitter":
                return "quitter"
            
            self.dessiner()
            self.horloge.tick(60)
        
        return "menu"