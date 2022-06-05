import random
from copy import deepcopy
from constants import NUM_CCS, CONSTRUCTION_CARDS

class ConstructionCardDeck():
    def __init__(self, card_lst: list) -> None:
        self._deck = deepcopy(card_lst)
        self._used_deck = []
        self._prev_cards = []
        self._curr_cards = []
        self.draw_new_cards()

    @property
    def curr_cards(self) -> list:
        return self._curr_cards

    def draw_new_cards(self) -> list:
        '''
        Draw three new ConstructionCards and return them in a list.
        '''
        new_cards = random.sample(self._deck, min(len(self._deck), NUM_CCS))
        for card in new_cards:
            self._deck.remove(card)
            self._used_deck.append(card)

        if not self._deck:
            self._deck, self._used_deck = self._used_deck, []

        self._prev_cards = self._curr_cards
        self._curr_cards = new_cards
        return new_cards

    def get_prev_card_effects(self) -> list:
        '''
        Return the effects from the cards that were just flipped.
        '''
        return [card[1] for card in self._prev_cards]


if __name__ == "__main__":
    cc = ConstructionCardDeck(CONSTRUCTION_CARDS)
    cc.draw_new_cards()
    print(cc.get_prev_card_effects())
