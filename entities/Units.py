from egg-fortress.entities.Egg import Egg

class Units() :

    # Constructeur par défaut
    def __init__(self , cost : int , speed : int , damage : int , hp : int , reward : int , position : tuple , owner : str ) :
        self.cost = cost
        self.speed = speed
        self.damage = damage
        self.hp = hp
        self.reward = reward
        self.position = position
        self.owner = owner

    ############################### Méthodes ###############################

    # Méthode d'attaque des unités
    def attackCible(self , cible : "Units" ) :
        cible.perteHp(self.damage)

    # Méthode d'attaque des oeufs
    def attackEgg(self , cible : "Egg") :
        cible.setLifePoints(cible.getLifePoints() - self.damage)
        
    ############################### Setters ###############################

    # Permet de soustraire des HP a l'unité 
    def perteHp(self , damage : int ) :
        self.hp -= damage

    # Permet de définir les HP de l'unité
    def setHp(self, hp: int):
        self.hp = hp

    # Permet de définir la position de l'unité
    def setPosition(self, position: tuple):
        self.position = position

    ############################### Getters ###############################

    # Permet de récupérer le cout de l'unité
    def getCost(self) -> int :
        return self.cost
    
    # Permet de récupérer la vitesse de l'unité
    def getSpeed(self) -> int :
        return self.speed
    
    # Permet de récupérer les dégats de l'unité
    def getDamage(self) -> int :
        return self.damage
    
    # Permet de récupérer les points de vie de l'unité
    def getHp(self) -> int :
        return self.hp
    
    # Permet de récupérer la récompense de l'unité
    def getReward(self) -> int :
        return self.reward
    
    # Permet de récupérer la position de l'unité
    def getPosition(self) -> tuple :
        return self.position
    
    # Permet de récupérer le propriétaire de l'unité
    def getOwner(self) -> str :
        return self.owner