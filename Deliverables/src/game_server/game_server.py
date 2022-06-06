import socket
import json
import sys
from typing import *
from . import ConstructionCardDeck, CityPlanDeck
from network import *
from players import *
from moves import MoveGenerator
from game_state import GameState

class GameServer():
    def __init__(self, game_config: Dict[str, int], local_players: List, cc_lst: List[List], cp_lst: List[Dict]) -> None:
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

    @property
    def players(self) -> List[Player]:
        return self._players

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

    def _add_local_players(self, local_players: List[Tuple[str, MoveGenerator]]) -> None:
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

    def play_game(self):
        while not self._is_game_over():
            self._all_players_play_move()

        self._send_final_scores()
        self._network.close()
        
    def _all_players_play_move(self):
        claimed_cps = set()
        for curr_player in self._players:
            if curr_player.cheated:
                continue

            curr_player.play_next_move(self._game_state)
            claimed_cps.update(curr_player.get_new_city_plan_scores())
            
        # update claimed city plans in GameState
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

    def _get_player_temps(self) -> List[int]:
        temps_lst = []
        for curr_player in self._players:
            if not curr_player.player_state:
                continue
            temps_lst.append(curr_player.player_state.temps)

        return temps_lst

    def calculate_player_scores(self) -> List[List]:
        temps_lst = self._get_player_temps()
        scores = []
        for curr_player in self._players:
            scores.append([curr_player.name, curr_player.get_score(temps_lst)])

        return scores

    def _send_final_scores(self) -> None:
        scores = self.calculate_player_scores()
        sys.stdout.write(json.dumps(scores))
        sys.stdout.flush()
        scores_dict = { "game-over": scores }
        for curr_player in self._players:
            curr_player.send_final_scores(scores_dict)

        