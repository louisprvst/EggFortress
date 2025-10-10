class Engine:
    def __init__(self, map, lap=1, lapNumber=1, money=0):
        self.map = map
        self.lap = lap
        self.lapNumber = lapNumber
        self.money = money

    def oneMoreLap(self, lap=1):
        self.lap = lap
        self.lapNumber += 1
        self.money += 15

    def getMap(self, map):
        return map

    def getLapNumber(self):
        return self.lapNumber

    # Prévue même si elle ne servira probablement pas comme définie dans oneMoreLap
    def setLapNumber(self, moreLap=1):
        self.lapNumber += moreLap

    def getMoney(self, money):
        return money

    def setMoney(self, money):
        self.money = money
