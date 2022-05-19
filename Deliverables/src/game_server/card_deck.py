import random

class CardDeck():
    def __init__(self, card_lst: list) -> None:
        self._deck = card_lst

    def draw_new_cards(self, num_cards: int) -> list:
        new_cards = random.sample(self._deck, min(len(self._deck), num_cards))
        for card in new_cards:
            self._deck.remove(card)

        return new_cards
