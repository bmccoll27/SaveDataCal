import cards


class Deck:
    def __init__(self, numberRemoved=0, numberDuplicated=0, saveDataValue=0):
        self.cards = []
        self.numberRemoved = numberRemoved
        self.numberDuplicated = numberDuplicated
        self.saveDataValue = saveDataValue
        self.removed_history = []
        self.pelanty = [0, 10, 30, 50]
        self.numberConverted = 0
        # allow building the default starting deck by forcing tier-0 adds
        self.add_card(name="Basic", cost=1, tier=0,
                      epiphany=False, divineEpiphany=False, force=True)
        self.add_card(name="Basic", cost=1, tier=0,
                      epiphany=False, divineEpiphany=False, force=True)
        self.add_card(name="Basic", cost=1, tier=0,
                      epiphany=False, divineEpiphany=False, force=True)

    def add_card(self, name, cost, tier, epiphany, divineEpiphany, duplicate=False, force=False):
        if tier == 0 and not force:
            raise ValueError("Adding tier 0 cards is not allowed")

        new_card = cards.Card(name=name,
                              cost=cost, tier=tier,
                              epiphany=epiphany, divineEpiphany=divineEpiphany, duplicate=duplicate, converted=False)
        self.load_save_data(new_card)
        self.cards.append(new_card)

    def load_save_data(self, card):
        if card.duplicate:
            if self.numberDuplicated <= len(self.pelanty):
                self.saveDataValue += self.pelanty[self.numberDuplicated]
            else:
                self.saveDataValue += 70
            self.numberDuplicated += 1
        if card.tier == 2 or card.tier == 4:
            self.saveDataValue += 20

        if card.tier == 3:
            self.saveDataValue += 80

        if card.epiphany and card.tier > 1:
            self.saveDataValue += 10

        if card.divineEpiphany:
            self.saveDataValue += 20

    def reload_save_data(self):
        self.saveDataValue = 0
        self.numberDuplicated = 0
        for card in self.cards:
            self.load_save_data(card)
        for amt in getattr(self, 'removed_history', []):
            self.saveDataValue += amt

    def remove_card(self, card):
        if card.tier == 0 or card.epiphany:
            extra = 20
        else:
            extra = 0
        if self.numberRemoved < len(self.pelanty):
            pen = self.pelanty[self.numberRemoved]
        else:
            pen = 70

        added = extra + pen
        self.saveDataValue += added
        self.removed_history.append(added)

        self.cards.remove(card)
        self.numberRemoved += 1

    def card_conversion_points(self, card):
        pass
        self.numberConverted += 1
        self.saveDataValue += self.numberConverted * 10

    def get_avg_cost(self):
        if not self.cards:
            return 0
        total_cost = sum(card.cost for card in self.cards)
        return total_cost / len(self.cards)

    def card_count(self):
        return len(self.cards)
