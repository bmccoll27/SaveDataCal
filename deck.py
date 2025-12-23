class Deck:
    def __init__(self, numberRemoved=0, saveDataValue=0):
        self.cards = []
        self.numberRemoved = numberRemoved
        self.saveDataValue = saveDataValue

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        card.addPoints(0)
        self.cards.remove(card)
        self.numberRemoved += 1

    def get_avg_cost(self):
        if not self.cards:
            return 0
        total_cost = sum(card.cost for card in self.cards)
        return total_cost / len(self.cards)
