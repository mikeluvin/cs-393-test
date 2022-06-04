from game_state import *
from player_state import *
from . import MoveGenerator

class SimpleMoveGenerator(MoveGenerator):
    '''
    Places the first house possible. Essentially a dumb player.
    '''
    def __init__(self, game_state: GameState, player_state: PlayerState) -> None:
        super().__init__(game_state, player_state)

    def generate_move(self) -> PlayerState:
        '''
        Returns a new PlayerState with a new house placed, or a refusal used.
        '''
        new_player_st = PlayerState(self.player_st.to_dict())
        for i, street in enumerate(new_player_st.streets):
            for ccard in self.game_st.ccards:
                locations = street.get_possible_home_locations(ccard.num)
                if locations:
                    street.homes[locations[0]].num = ccard.num
                    return new_player_st

        # if we get here, we weren't able to place a home
        new_player_st.refusals += 1
        return new_player_st


