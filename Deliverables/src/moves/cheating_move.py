from game_state import *
from player_state import *
from . import MoveGenerator

class CheatingMoveGenerator(MoveGenerator):
    '''
    A cheating player. Returns the same player state it was given.
    '''
    def __init__(self, game_state: GameState, player_state: PlayerState) -> None:
        super().__init__(game_state, player_state)

    def generate_move(self) -> PlayerState:
        '''
        Returns the same PlayerState.
        '''
        return self.player_st


