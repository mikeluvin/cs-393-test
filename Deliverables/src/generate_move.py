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
        new_player_st = PlayerState(self.player_st.to_dict())
        for i in range(len(new_player_st.streets)):
            street = new_player_st.streets[i]
            for j in range(len(street.homes)):
                if street.homes[j].num == "blank":
                    # try to play each of the construction cards
                    for ccard in self.game_st.ccards:
                        try:
                            # try setting home with the new number
                            street.try_place_new_home(j, ccard.num)
                        except StreetException:
                            # change home number back to "blank"
                            street.try_place_new_home(j, "blank")
                        else:
                            # then, we were able to place the home
                            return new_player_st
        # if we get here, we weren't able to place a home
        new_player_st.refusals += 1
        return new_player_st


