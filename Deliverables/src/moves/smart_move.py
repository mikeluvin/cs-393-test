from math import floor
from game_state import *
from player_state import *
from exception import *
from constants import MAX_ROUNDABOUTS, STREET_LENS
from . import MoveGenerator

class SmartMoveGenerator(MoveGenerator):
    '''
    Makes a smart move.
    '''
    def __init__(self, game_state: GameState, player_state: PlayerState) -> None:
        super().__init__(game_state, player_state)

    def generate_move(self) -> PlayerState:
        '''
        Returns a new PlayerState with a new house placed, or a refusal used.
        '''
        new_ps = PlayerState(self.player_st.to_dict())
        all_locations = []

        # place both roundabouts immediately?
        if new_ps.roundabouts < MAX_ROUNDABOUTS:
            self.try_place_roundabout(new_ps)

        for ccard in self.game_st.ccards:
            curr_card_locations = []
            for i, street in enumerate(new_ps.streets):
                curr_card_locations.append(street.get_possible_home_locations(ccard.num))
                if curr_card_locations[i]:
                    street.homes[curr_card_locations[i][0]].num = ccard.num
                    return new_ps
            
            all_locations.append(curr_card_locations)

        # if we get here, we weren't able to place a home
        new_ps.refusals += 1
        return new_ps

    def try_place_roundabout(self, new_ps: PlayerState):
        # decided limit one roundabout per street
        for i, street in enumerate(new_ps.streets):
            if street.roundabout_count() == 0:
                idx = floor(STREET_LENS[i] / 2)
                try:
                    street.place_roundabout(idx)
                    return
                except HomeException:
                    pass

                # try to place one house to the left
                try:
                    street.place_roundabout(idx - 1)
                    return
                except HomeException:
                    pass





