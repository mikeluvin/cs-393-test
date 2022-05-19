import random

class CityPlanDeck():
    def __init__(self, card_lst: list) -> None:
        self._decks = self._separate_cards_by_position(card_lst)

    def _separate_cards_by_position(self, card_lst: list) -> dict:
        decks = { 1: [], 2: [], 3: [] }
        for card in card_lst:
            decks[card["position"]].append(card)

        return decks

    def draw_new_cards(self) -> list:
        new_cards = []
        for deck in self._decks.values():
            card = random.choice(deck)
            new_cards.append(card)
            deck.remove(card)

        return new_cards
