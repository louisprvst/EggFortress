class Egg:
    def __init__(self, position: tuple, size=1, life_points=1000):
        self.position = position
        self.lifePoints = life_points
        self.size = size
        self.isBroken = False

    def breakEgg(self):
        if not self.isBroken:
            self.isBroken = True

    def getLifePoints(self):
        return self.lifePoints

    def setLifePoints(self, life_points):
        self.lifePoints = life_points