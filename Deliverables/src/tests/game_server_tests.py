import unittest
from game_server import *
from constants import CONSTRUCTION_CARDS, CITY_PLAN_CARDS

class TestConstructionCardDeck(unittest.TestCase):
    def test_draw_construction_cards(self):
        deck = ConstructionCardDeck(CONSTRUCTION_CARDS)
        new_cards = deck.draw_new_cards()
        self.assertTrue(all([card in CONSTRUCTION_CARDS for card in new_cards]))

    def test_prev_card_effects(self):
        deck = ConstructionCardDeck(CONSTRUCTION_CARDS)
        prev_card_effects = [card[1] for card in deck.curr_cards]
        deck.draw_new_cards()
        self.assertEqual(deck.get_prev_card_effects(), prev_card_effects)

class TestCityPlanDeck(unittest.TestCase):
    def test_separate_cards(self):
        cp_list = [
            {
                "criteria": [1,1,2,6],
                "position": 1,
                "score1": 8,
                "score2": 4
            },
            {
                "criteria": [1,1,1,1],
                "position": 2,
                "score1": 8,
                "score2": 4
            },
            {
                "criteria": [1,2,3],
                "position": 3,
                "score1": 8,
                "score2": 4
            }
        ]
        cp_deck = CityPlanDeck(cp_list)
        deck = { 
            1: [cp_list[0]], 
            2: [cp_list[1]],
            3: [cp_list[2]] 
        }
        self.assertEqual(cp_deck.decks, deck)
        
    def test_draw_cp_cards(self):
        cp_deck = CityPlanDeck(CITY_PLAN_CARDS)
        new_cards = cp_deck.draw_new_cards()
        self.assertTrue(all([card in CITY_PLAN_CARDS for card in new_cards]))
        positions = set([card["position"] for card in new_cards])
        self.assertEqual(positions, set([1,2,3]))
    
if __name__ == "__main__":
    unittest.main()
