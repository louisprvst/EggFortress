import os
import pygame
import sys

class Menu:
    def __init__(self, ecran):
        self.ecran = ecran
        self.largeur = ecran.get_width()
        self.hauteur = ecran.get_height()
        self.running = True
        self.horloge = pygame.time.Clock()
        
        # Couleurs
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS = (128, 128, 128)
        self.GRIS_CLAIR = (200, 200, 200)
        
        # Charger les ressources
        self._charger_assets()
        self._creer_boutons()
        
    def _charger_assets(self):
        """Charge les images et polices"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        menu_assets_dir = os.path.join(script_dir, "..", "assets", "images", "Menu")
        
        self.background = pygame.image.load(os.path.join(menu_assets_dir, "background.jpg"))
        self.background = pygame.transform.scale(self.background, (self.largeur, self.hauteur))
        
        self.logo = pygame.image.load(os.path.join(menu_assets_dir, "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (450, 225))
        
        # Polices
        self.font_bouton = pygame.font.Font(None, 36)
        self.font_titre = pygame.font.Font(None, 64)
        self.font_sous_titre = pygame.font.Font(None, 48)
        self.font_noms = pygame.font.Font(None, 42)
        
    def _creer_boutons(self):
        """Crée les boutons du menu"""
        self.bouton_jouer = pygame.Rect(self.largeur//2 - 100, self.hauteur//2 + 50, 200, 60)
        self.bouton_credits = pygame.Rect(self.largeur//2 - 100, self.hauteur//2 + 120, 200, 60)
        self.bouton_quitter = pygame.Rect(self.largeur//2 - 100, self.hauteur//2 + 190, 200, 60)
        
        # Position du logo
        self.logo_x = self.largeur//2 - self.logo.get_width()//2
        self.logo_y = self.hauteur//2 - 250

    def _dessiner_bouton(self, rect, texte, couleur_fond, couleur_texte):
        """Dessine un bouton avec du texte"""
        pygame.draw.rect(self.ecran, couleur_fond, rect)
        pygame.draw.rect(self.ecran, self.NOIR, rect, 3)  
        
        texte_surface = self.font_bouton.render(texte, True, couleur_texte)
        texte_x = rect.x + (rect.width - texte_surface.get_width()) // 2
        texte_y = rect.y + (rect.height - texte_surface.get_height()) // 2
        self.ecran.blit(texte_surface, (texte_x, texte_y))
    
    def afficher_credits(self):
        """Affiche l'écran des crédits"""
        bouton_retour = pygame.Rect(50, self.hauteur - 100, 150, 50)
        credits_running = True
        
        developpeurs = [
            "TELLIEZ Luc",
            "FARDEL Mathéïs", 
            "PREVOST Louis",
            "EL MOUTAOUAKIL Nadir",
            "DELDALLE Corentin"
        ]
        
        while credits_running:
            pos_souris = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_retour.collidepoint(pos_souris):
                        credits_running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        credits_running = False
            
            # Dessiner le fond
            self.ecran.blit(self.background, (0, 0))
            
            # Calculer les dimensions du cadre blanc
            titre = self.font_titre.render("CRÉDITS", True, self.NOIR)
            texte_dev = self.font_sous_titre.render("Développé par :", True, self.NOIR)
            
            # Calculer la largeur maximale nécessaire
            largeur_max = max(titre.get_width(), texte_dev.get_width())
            for dev in developpeurs:
                texte_nom = self.font_noms.render(f"• {dev}", True, self.NOIR)
                largeur_max = max(largeur_max, texte_nom.get_width())
            
            # Dimensions du cadre blanc avec marge
            marge = 40
            cadre_largeur = largeur_max + marge * 2
            cadre_hauteur = 400  # Hauteur fixe pour englober tout
            cadre_x = self.largeur//2 - cadre_largeur//2
            cadre_y = self.hauteur//2 - cadre_hauteur//2
            
            # Dessiner le cadre blanc avec bordure
            cadre_rect = pygame.Rect(cadre_x, cadre_y, cadre_largeur, cadre_hauteur)
            pygame.draw.rect(self.ecran, self.BLANC, cadre_rect)
            pygame.draw.rect(self.ecran, self.NOIR, cadre_rect, 3)  # Bordure noire
            
            # Centre du cadre pour le positionnement
            centre_cadre_x = cadre_x + cadre_largeur//2
            centre_cadre_y = cadre_y + cadre_hauteur//2
            
            # Titre - positionné en haut du cadre
            titre_x = centre_cadre_x - titre.get_width()//2
            titre_y = cadre_y + 30
            self.ecran.blit(titre, (titre_x, titre_y))
            
            # Sous-titre - sous le titre
            sous_titre_x = centre_cadre_x - texte_dev.get_width()//2
            sous_titre_y = titre_y + 80
            self.ecran.blit(texte_dev, (sous_titre_x, sous_titre_y))
            
            # Liste des développeurs - centrée verticalement dans l'espace restant
            nb_devs = len(developpeurs)
            hauteur_totale_devs = nb_devs * 45
            y_start_devs = sous_titre_y + 60
            
            for i, dev in enumerate(developpeurs):
                texte_nom = self.font_noms.render(f"• {dev}", True, self.NOIR)
                nom_x = centre_cadre_x - texte_nom.get_width()//2
                nom_y = y_start_devs + i * 45
                self.ecran.blit(texte_nom, (nom_x, nom_y))
            
            # Bouton retour
            if bouton_retour.collidepoint(pos_souris):
                self._dessiner_bouton(bouton_retour, "RETOUR", self.GRIS_CLAIR, self.NOIR)
            else:
                self._dessiner_bouton(bouton_retour, "RETOUR", self.BLANC, self.NOIR)
            
            # Instructions
            instruction = self.font_noms.render("Appuyez sur ESC ou cliquez sur RETOUR", True, self.GRIS)
            self.ecran.blit(instruction, (self.largeur//2 - instruction.get_width()//2, self.hauteur - 50))
            
            pygame.display.flip()
            self.horloge.tick(60)
    
    def gerer_evenements(self):
        """Gère les événements du menu"""
        pos_souris = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bouton_jouer.collidepoint(pos_souris):
                    return "jouer"
                elif self.bouton_credits.collidepoint(pos_souris):
                    self.afficher_credits()
                elif self.bouton_quitter.collidepoint(pos_souris):
                    self.running = False
        
        return None
    
    def dessiner(self):
        """Dessine le menu"""
        pos_souris = pygame.mouse.get_pos()
        
        # Fond et logo
        self.ecran.blit(self.background, (0, 0))
        self.ecran.blit(self.logo, (self.logo_x, self.logo_y))
        
        # Boutons avec effet de survol
        if self.bouton_jouer.collidepoint(pos_souris):
            self._dessiner_bouton(self.bouton_jouer, "JOUER", self.GRIS_CLAIR, self.NOIR)
        else:
            self._dessiner_bouton(self.bouton_jouer, "JOUER", self.BLANC, self.NOIR)
        
        if self.bouton_credits.collidepoint(pos_souris):
            self._dessiner_bouton(self.bouton_credits, "CRÉDITS", self.GRIS_CLAIR, self.NOIR)
        else:
            self._dessiner_bouton(self.bouton_credits, "CRÉDITS", self.BLANC, self.NOIR)
        
        if self.bouton_quitter.collidepoint(pos_souris):
            self._dessiner_bouton(self.bouton_quitter, "QUITTER", self.GRIS_CLAIR, self.NOIR)
        else:
            self._dessiner_bouton(self.bouton_quitter, "QUITTER", self.BLANC, self.NOIR)
        
        pygame.display.flip()
    
    def executer(self):
        """Boucle principale du menu"""
        while self.running:
            action = self.gerer_evenements()
            if action == "jouer":
                return "jouer" 
            
            self.dessiner()
            self.horloge.tick(60)
        
        return "quitter"