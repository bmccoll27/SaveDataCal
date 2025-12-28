class Card:
    def __init__(self, name, cost, tier, epiphany, divineEpiphany, points=0, duplicate=False, converted=False):
        self.name = name
        self.cost = cost
        self.tier = tier
        self.epiphany = epiphany
        self.divineEpiphany = divineEpiphany
        self.duplicate = duplicate
        self.points = points
        self.converted = converted

    def total_points(self):
        if self.tier == 2:
            points = 20
        if self.tier == 3:
            points = 80
        if self.epiphany:
            points += 10
        if self.divineEpiphany:
            points += 20
        return points

    def setPoints(self, points):
        self.points = points

    def addPoints(self, points):
        self.points += points

    def subtactPoints(self, points):
        self.points -= points

    def __str__(self):
        return f"Card(cost={self.cost}, tier={self.tier}, epiphany={self.epiphany}, divineEpiphany={self.divineEpiphany})"
