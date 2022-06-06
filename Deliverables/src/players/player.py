from typing import List
from game_state import GameState
from player_state import PlayerState
from moves import MoveValidator
from exception import MoveException

class Player():
    def __init__(self, name:str) -> None:
        self._player_state = PlayerState()
        self._prev_ps = PlayerState()
        self._name = name
        self.cheated = False

    @property
    def name(self):
        return self._name

    @property
    def player_state(self) -> PlayerState:
        '''
        Returns this player's PlayerState, or False if they cheated.
        '''
        return self._player_state

    @property
    def prev_ps(self) -> PlayerState:
        return self._prev_ps

    @player_state.setter
    def player_state(self, player_state: PlayerState) -> None:
        self._player_state = player_state

    def play_next_move(self, game_state: GameState) -> None:
        '''
        Given a GameState, get the player's next move and update self.player_state
        their new PlayerState, or False if they cheated.
        '''
        self._prev_ps = self._player_state
        new_ps = self._get_next_player_state(game_state)

        try:
            MoveValidator(game_state, self._player_state, new_ps).validate_move()
            self._player_state = new_ps
        except MoveException:
            self._set_cheater()

    def _get_next_player_state(self, game_state: GameState) -> PlayerState:
        '''
        Given a GameState, get the player's new player state. Returns
        their new PlayerState, (or False if they disconnected or sent
        an invalid PlayerState, only possible with the NetworkPlayer).
        '''
        raise NotImplementedError()

    def get_new_city_plan_scores(self) -> List[int]:
        '''
        Find newly claimed city plan scores from prev_ps to new_ps and add 
        their indices to claimed_cps set.
        '''
        if not self._player_state:
            return set()

        claimed_cps = set()
        for cp_idx, score in enumerate(self._player_state.city_plan_score):
            prev_cp_score = self._prev_ps.city_plan_score[cp_idx]
            if prev_cp_score == "blank" and score != "blank":
                claimed_cps.add(cp_idx)

        return claimed_cps

    def _set_cheater(self):
        self._player_state = False
        self.cheated = True
        self.close()
    
    def close(self):
        pass

    def send_final_scores(self, scores: dict):
        pass

    def get_score(self, temps_lst: list):
        return self._player_state.calculate_score(temps_lst) if self._player_state else False

    def __eq__(self, other: object) -> bool:
        return other.player_state == self._player_state and other.name == self._name and other.cheated == self.cheated