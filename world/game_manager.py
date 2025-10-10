class GameManager:
    """Gère le système de tour par tour et les phases de jeu"""
    
    def __init__(self):
        # Joueurs
        self.joueur1 = {"nom": "Joueur 1", "couleur": "bleu", "oeufs_places": 0, "dinosaures_places": 0}
        self.joueur2 = {"nom": "Joueur 2", "couleur": "rouge", "oeufs_places": 0, "dinosaures_places": 0}
        
        # État du jeu
        self.joueur_actuel = self.joueur1
        self.phase_actuelle = "placement_oeufs"  # "placement_oeufs", "placement_dinosaures", "combat"
        self.tour_numero = 1
        
        # Limites de placement
        self.max_oeufs_par_joueur = 1
        self.max_dinosaures_par_joueur = 5
        
        # Historique des actions
        self.historique = []
    
    def get_joueur_actuel(self):
        """Retourne le joueur actuel"""
        return self.joueur_actuel
    
    def get_phase_actuelle(self):
        """Retourne la phase actuelle"""
        return self.phase_actuelle
    
    def get_tour_numero(self):
        """Retourne le numéro du tour"""
        return self.tour_numero
    
    def get_elements_autorises(self):
        """Retourne les éléments que le joueur actuel peut placer"""
        if self.phase_actuelle == "placement_oeufs":
            if self.joueur_actuel["oeufs_places"] < self.max_oeufs_par_joueur:
                if self.joueur_actuel["couleur"] == "bleu":
                    return ["oeuf_bleu"]
                else:
                    return ["oeuf_rouge"]
            return []
        
        elif self.phase_actuelle == "placement_dinosaures":
            if self.joueur_actuel["dinosaures_places"] < self.max_dinosaures_par_joueur:
                if self.joueur_actuel["couleur"] == "bleu":
                    return ["diplodocus_bleu", "parasaure_bleu", "trex_bleu"]
                else:
                    return ["diplodocus_rouge", "parasaure_rouge", "trex_rouge"]
            return []
        
        return []
    
    def peut_placer_element(self, type_element):
        """Vérifie si le joueur peut placer cet élément"""
        elements_autorises = self.get_elements_autorises()
        return type_element in elements_autorises
    
    def placer_element(self, type_element):
        """Enregistre le placement d'un élément et met à jour les compteurs"""
        if not self.peut_placer_element(type_element):
            return False
        
        # Mettre à jour les compteurs
        if type_element in ["oeuf_bleu", "oeuf_rouge"]:
            self.joueur_actuel["oeufs_places"] += 1
        elif type_element in ["diplodocus_bleu", "parasaure_bleu", "trex_bleu", 
                             "diplodocus_rouge", "parasaure_rouge", "trex_rouge"]:
            self.joueur_actuel["dinosaures_places"] += 1
        
        # Ajouter à l'historique
        self.historique.append({
            "joueur": self.joueur_actuel["nom"],
            "element": type_element,
            "phase": self.phase_actuelle,
            "tour": self.tour_numero
        })
        
        return True
    
    def passer_au_suivant(self):
        """Passe au joueur/phase suivant"""
        if self.phase_actuelle == "placement_oeufs":
            # Phase placement des œufs
            if self.joueur_actuel == self.joueur1:
                # Si joueur 1 vient de jouer, passer au joueur 2
                if self.joueur1["oeufs_places"] < self.max_oeufs_par_joueur:
                    self.joueur_actuel = self.joueur2
                else:
                    # Joueur 1 a fini ses œufs, vérifier joueur 2
                    if self.joueur2["oeufs_places"] < self.max_oeufs_par_joueur:
                        self.joueur_actuel = self.joueur2
                    else:
                        # Les deux ont fini, passer à la phase dinosaures
                        self._passer_phase_dinosaures()
            else:
                # Si joueur 2 vient de jouer
                if self.joueur2["oeufs_places"] < self.max_oeufs_par_joueur:
                    # Vérifier si joueur 1 peut encore jouer
                    if self.joueur1["oeufs_places"] < self.max_oeufs_par_joueur:
                        self.joueur_actuel = self.joueur1
                    # Sinon rester sur joueur 2
                else:
                    # Joueur 2 a fini, vérifier joueur 1
                    if self.joueur1["oeufs_places"] < self.max_oeufs_par_joueur:
                        self.joueur_actuel = self.joueur1
                    else:
                        # Les deux ont fini, passer à la phase dinosaures
                        self._passer_phase_dinosaures()
        
        elif self.phase_actuelle == "placement_dinosaures":
            # Phase placement des dinosaures
            if self.joueur_actuel == self.joueur1:
                self.joueur_actuel = self.joueur2
            else:
                self.joueur_actuel = self.joueur1
                self.tour_numero += 1
            
            # Vérifier si la phase dinosaures est terminée
            if (self.joueur1["dinosaures_places"] >= self.max_dinosaures_par_joueur and 
                self.joueur2["dinosaures_places"] >= self.max_dinosaures_par_joueur):
                self._passer_phase_combat()
    
    def _passer_phase_dinosaures(self):
        """Passe à la phase de placement des dinosaures"""
        self.phase_actuelle = "placement_dinosaures"
        self.joueur_actuel = self.joueur1  # Joueur 1 commence les dinosaures
        self.tour_numero = 1
    
    def _passer_phase_combat(self):
        """Passe à la phase de combat"""
        self.phase_actuelle = "combat"
        # Pour l'instant, on ne fait rien de spécial pour le combat
    
    def est_phase_terminee(self):
        """Vérifie si la phase actuelle est terminée"""
        if self.phase_actuelle == "placement_oeufs":
            return (self.joueur1["oeufs_places"] >= self.max_oeufs_par_joueur and 
                    self.joueur2["oeufs_places"] >= self.max_oeufs_par_joueur)
        
        elif self.phase_actuelle == "placement_dinosaures":
            return (self.joueur1["dinosaures_places"] >= self.max_dinosaures_par_joueur and 
                    self.joueur2["dinosaures_places"] >= self.max_dinosaures_par_joueur)
        
        return False
    
    def get_status_text(self):
        """Retourne le texte de statut du jeu"""
        if self.phase_actuelle == "placement_oeufs":
            return f"Phase: Placement des œufs - {self.joueur_actuel['nom']} à vous de jouer!"
        elif self.phase_actuelle == "placement_dinosaures":
            return f"Tour {self.tour_numero} - Phase: Placement des dinosaures - {self.joueur_actuel['nom']} à vous de jouer!"
        elif self.phase_actuelle == "combat":
            return "Phase: Combat - Jeu terminé!"
        
        return "Jeu en cours..."
    
    def get_compteurs_text(self):
        """Retourne le texte des compteurs"""
        return [
            f"Joueur 1 (Bleu): {self.joueur1['oeufs_places']}/{self.max_oeufs_par_joueur} œufs, {self.joueur1['dinosaures_places']}/{self.max_dinosaures_par_joueur} dinosaures",
            f"Joueur 2 (Rouge): {self.joueur2['oeufs_places']}/{self.max_oeufs_par_joueur} œufs, {self.joueur2['dinosaures_places']}/{self.max_dinosaures_par_joueur} dinosaures"
        ]
    
    def reset(self):
        """Remet le jeu à zéro"""
        self.joueur1 = {"nom": "Joueur 1", "couleur": "bleu", "oeufs_places": 0, "dinosaures_places": 0}
        self.joueur2 = {"nom": "Joueur 2", "couleur": "rouge", "oeufs_places": 0, "dinosaures_places": 0}
        self.joueur_actuel = self.joueur1
        self.phase_actuelle = "placement_oeufs"
        self.tour_numero = 1
        self.historique = []