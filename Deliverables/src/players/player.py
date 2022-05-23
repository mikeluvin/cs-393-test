from game_state import GameState
from player_state import PlayerState

class Player():
    def __init__(self, name:str) -> None:
        self._player_state = PlayerState()
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def player_state(self) -> PlayerState:
        '''
        Returns this player's PlayerState, or False if they cheated.
        '''
        return self._player_state

    @player_state.setter
    def player_state(self, player_state: PlayerState) -> None:
        self._player_state = player_state

    def get_next_move(self, game_state: GameState):
        '''
        Given a GameState, get the player's next move and return
        their new PlayerState.
        '''
        raise NotImplementedError()
    
    def close(self):
        pass

    def send_final_scores(self, scores: dict):
        pass

    def get_score(self, temps_lst: list):
        return self._player_state.calculate_score(temps_lst) if self._player_state else False