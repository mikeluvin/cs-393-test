import unittest
from game_server import *
from moves import CheatingMoveGenerator, SimpleMoveGenerator
from players import LocalPlayer
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


class TestGameServer(unittest.TestCase):
    def test_init_local_players(self):
        local_players = [
            ("p1", SimpleMoveGenerator),
            ("p2", SimpleMoveGenerator)
        ]
        network_config = { "players": 0, "port": 8080 }
        server = GameServer(network_config, local_players, CONSTRUCTION_CARDS, CITY_PLAN_CARDS)
        server._network.close()
        init_players = []
        for player_name, move_generator in local_players:
            init_players.append(LocalPlayer(player_name, move_generator))

        self.assertEqual(init_players, server.players)

    def test_all_players_play_move(self):
        local_players = [
            ("p1", SimpleMoveGenerator),
            ("p2", SimpleMoveGenerator)
        ]
        network_config = { "players": 0, "port": 8080 }
        server = GameServer(network_config, local_players, CONSTRUCTION_CARDS, CITY_PLAN_CARDS)
        server._network.close()
        server._all_players_play_move()
        for curr_player in server.players:
            self.assertFalse(curr_player.cheated)
            self.assertNotEqual(curr_player.prev_ps, curr_player.player_state)
    
if __name__ == "__main__":
    unittest.main()
