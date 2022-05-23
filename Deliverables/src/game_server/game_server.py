import socket
import json

from . import ConstructionCardDeck, CityPlanDeck
from network import *
from players import *
from moves import MoveValidator
from exception import MoveException
from game_state import GameState
import sys

class GameServer():
    def __init__(self, game_config: dict, local_players: list, cc_lst: list, cp_lst: list) -> None:
        self._num_network_players = game_config["players"]
        self._port = game_config["port"]
        self._cc_deck = ConstructionCardDeck(cc_lst)
        self._cp_deck = CityPlanDeck(cp_lst)
        # list of Player objects
        self._players = []
        self._game_state = self._initialize_game_state()
        self._start_tcp_listener()
        self._connect_to_network_players()
        self._add_local_players(local_players)
        self._play_game()

    def _start_tcp_listener(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(('', self._port))
        self._sock.listen()
        self._network = NetworkAdapter(self._sock)
        sys.stdout.write(json.dumps("started"))
        sys.stdout.flush()

    def _connect_to_network_players(self):
        while len(self._players) < self._num_network_players:
            player_sock, addr = self._sock.accept()
            self._players.append(NetworkPlayer(player_sock, addr))

    def _add_local_players(self, local_players: list) -> None:
        for player_name, move_generator in local_players:
            self._players.append(LocalPlayer(player_name, move_generator))

    def _initialize_game_state(self) -> GameState:
        curr_ccs = self._cc_deck.draw_new_cards()
        prev_cc_effects = self._cc_deck.get_prev_card_effects()
        city_plan_cards = self._cp_deck.draw_new_cards()
        gs_dict = {
            "city-plans": city_plan_cards,
            "city-plans-won": [False, False, False],
            "construction-cards": curr_ccs,
            "effects": prev_cc_effects
        }
        return GameState(gs_dict)

    def _draw_new_construction_cards(self) -> None:
        curr_ccs = self._cc_deck.draw_new_cards()
        prev_cc_effects = self._cc_deck.get_prev_card_effects()
        self._game_state.ccards = curr_ccs
        self._game_state.effects = prev_cc_effects

    def _play_game(self):
        while not self._is_game_over():
            self._play_move()

        scores = self._calculate_player_scores()
        sys.stdout.write(json.dumps(scores))
        sys.stdout.flush()
        self._send_final_scores({ "game-over": scores })
        self._network.close()
        
    def _play_move(self):
        claimed_cps = set()
        for curr_player in self._players:
            # player_state is False if they cheated, so skip them
            if not curr_player.player_state:
                continue

            new_ps = curr_player.get_next_move(self._game_state)
            if new_ps:
                try:
                    move_validator = MoveValidator(self._game_state, curr_player.player_state, new_ps)
                    move_validator.validate_move()
                except MoveException:
                    new_ps = False

            # if the new PlayerState is False, then the player cheated
            if not new_ps:
                curr_player.close()
            else:
                # find newly claimed city plans
                for cp_idx, _ in move_validator.new_city_plans():
                    claimed_cps.add(cp_idx)
                
            curr_player.player_state = new_ps

        # updated claimed city plans in GameState
        for i in claimed_cps:
            self._game_state.city_plans_won[i] = True

        self._draw_new_construction_cards()

    def _is_game_over(self) -> bool:
        for curr_player in self._players:
            if not curr_player.player_state:
                continue
            if curr_player.player_state.is_game_over():
                return True

        return False

    def _get_player_temps(self):
        temps_lst = []
        for curr_player in self._players:
            if not curr_player.player_state:
                continue
            temps_lst.append(curr_player.player_state.temps)
        return temps_lst

    def _calculate_player_scores(self) -> list:
        temps_lst = self._get_player_temps()
        scores = []
        for curr_player in self._players:
            scores.append([curr_player.name, curr_player.get_score(temps_lst)])

        return scores

    def _send_final_scores(self, scores: list) -> None:
        for curr_player in self._players:
            curr_player.send_final_scores(scores)

        