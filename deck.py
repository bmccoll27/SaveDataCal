import cards


class Deck:
    def __init__(self, numberRemoved=0, numberDuplicated=0, saveDataValue=0):
        self.cards = []
        self.numberRemoved = numberRemoved
        self.numberDuplicated = numberDuplicated
        self.saveDataValue = saveDataValue
        self.pelanty = [0, 10, 30, 50]
        # allow building the default starting deck by forcing tier-0 adds
        self.add_card(name="Strike", cost=1, tier=0,
                      epiphany=False, divineEpiphany=False, force=True)
        self.add_card(name="Strike", cost=1, tier=0,
                      epiphany=False, divineEpiphany=False, force=True)
        self.add_card(name="Defend", cost=1, tier=0,
                      epiphany=False, divineEpiphany=False, force=True)

    def add_card(self, name, cost, tier, epiphany, divineEpiphany, duplicate=False, force=False):
        if tier == 0 and not force:
            raise ValueError("Adding tier 0 cards is not allowed")

        new_card = cards.Card(name=name,
                              cost=cost, tier=tier,
                              epiphany=epiphany, divineEpiphany=divineEpiphany, duplicate=duplicate)
        if new_card.duplicate:
            self.numberDuplicated += 1
            if self.numberDuplicated <= len(self.pelanty):
                self.saveDataValue += self.pelanty[self.numberDuplicated - 1]
            else:
                self.saveDataValue += 70

        self.cards.append(new_card)

    def remove_card(self, card):
        if card.tier == 0:
            self.saveDataValue += 20

        if self.numberRemoved < len(self.pelanty):
            self.saveDataValue += self.pelanty[self.numberRemoved]
        else:
            self.saveDataValue += 70

        self.cards.remove(card)
        self.numberRemoved += 1

    def get_avg_cost(self):
        if not self.cards:
            return 0
        total_cost = sum(card.cost for card in self.cards)
        return total_cost / len(self.cards)

    def card_count(self):
        return len(self.cards)
