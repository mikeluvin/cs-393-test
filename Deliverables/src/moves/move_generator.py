from game_state import *
from player_state import *

class MoveGenerator():
    def __init__(self, game_state: GameState, player_state: PlayerState) -> None:
        self.game_st = game_state
        self.player_st = player_state

    def generate_move(self) -> PlayerState:
        '''
        Returns a new PlayerState with a new house placed, or a refusal used.
        '''
        raise NotImplementedError()


