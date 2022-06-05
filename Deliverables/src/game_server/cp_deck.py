import random
from typing import *
from exception import CardDeckException, my_assert
from helpers import check_valid_lst

class CityPlanDeck():
    def __init__(self, card_lst: List[Dict]) -> None:
        self._decks = self._separate_cards_by_position(card_lst)

    @property
    def decks(self) -> Dict[int, List[Dict]]:
        return self._decks

    def _separate_cards_by_position(self, card_lst: List[Dict]) -> Dict[int, List[Dict]]:
        posns = set([1,2,3])
        my_assert(check_valid_lst(card_lst, None, lambda card: type(card) == dict and card.get("position", -1) in posns),
            CardDeckException,
            "Must provide a list of dictionaries with the 'position' field.")
        decks = { 1: [], 2: [], 3: [] }
        for card in card_lst:
            decks[card["position"]].append(card)

        return decks

    def draw_new_cards(self) -> List[Dict]:
        new_cards = []
        for deck in self._decks.values():
            card = random.choice(deck)
            new_cards.append(card)
            deck.remove(card)

        return new_cards
