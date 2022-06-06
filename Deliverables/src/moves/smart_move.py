from math import floor
from copy import deepcopy
import random
from typing import *
from game_state import *
from player_state import *
from exception import *
from constants import MAX_ROUNDABOUTS, STREET_LENS, POOL_LOCS, AGENT_MAXES, MAX_TEMPS, MAX_REFUSALS
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
        new_player_states = []

        # place both roundabouts immediately
        if new_ps.roundabouts < MAX_ROUNDABOUTS:
            self.try_place_roundabout(new_ps)

        for card_idx, ccard in enumerate(self.game_st.ccards):
            # try playing the effect corresponding to this construction card
            effect = self.game_st.effects[card_idx]
            for i, street in enumerate(new_ps.streets):
                locations = dict()
                if effect == "temp" and new_ps.temps < MAX_TEMPS:
                    possible_nums = [max(ccard.num + x, 0) for x in range(-2, 3)]
                else: 
                    possible_nums = [ccard.num]

                for num in possible_nums:
                    locations[num] = street.get_possible_home_locations(num)

                for num, home_indices in locations.items():
                    for home_idx in home_indices:
                        new_player_states.extend(self.create_new_ps_with_home_and_effect(new_ps, i, home_idx, num, effect))
        
        if not new_player_states:
            # if we get here, we weren't able to place a home
            new_ps.refusals += 1
            return new_ps

        return self.get_best_move(new_player_states)


    def try_place_roundabout(self, old_ps: PlayerState):
        new_ps = deepcopy(old_ps)
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

    def create_new_ps_with_home_and_effect(self, old_ps: PlayerState, st_idx: int, home_idx: int, num: int, effect: Effect) -> List[PlayerState]:
        new_ps = deepcopy(old_ps)
        new_ps.streets[st_idx].homes[home_idx].num = num
        new_ps_lst = [new_ps]

        if effect == "temp":
            try:
                new_ps.temps += 1
            except PlayerStateException:
                pass
        elif effect == "landscaper":
            try:
                new_ps.streets[st_idx].parks += 1
            except PlayerStateException:
                pass
        elif effect == "agent":
            try:
                agents = new_ps.agents
                # try to max out estates of size 5
                pattern = [4, 3, 2, 5, 1, 0]
                for i in pattern:
                    if agents[i] < AGENT_MAXES[i]:
                        agents[i] += 1
                        break
                new_ps.agents = agents
            except PlayerStateException:
                pass
        elif effect == "pool":
            if home_idx in POOL_LOCS[st_idx]:
                pool_idx = POOL_LOCS[st_idx].index(home_idx)
                new_ps.streets[st_idx].pools[pool_idx] = True
        elif effect == "surveyor":
            # only try to build fences in the third street
            # try to split into estates of size 4
            desired_st = 2
            for i in [3, 7]:
                if not new_ps.streets[desired_st].has_fence(i):
                    new_ps.streets[desired_st].place_fence(i)
                    break
        elif effect == "bis":
            street = new_ps.streets[st_idx]
            curr_home = street.homes[home_idx]
            second_ps = deepcopy(new_ps)
            if home_idx < STREET_LENS[st_idx] - 1 and street.homes[home_idx + 1].num == "blank" and not curr_home.fence_right:
                street.homes[home_idx + 1].num = num
                street.homes[home_idx + 1].is_bis = True

            street2 = second_ps.streets[st_idx]
            curr_home = street2.homes[home_idx]
            if home_idx > 0 and street2.homes[home_idx - 1].num == "blank" and not curr_home.fence_left:
                street2.homes[home_idx - 1].num = num
                street2.homes[home_idx - 1].is_bis = True
                new_ps_lst.append(second_ps)

        return new_ps_lst
        
    def get_best_move(self, player_states: List[PlayerState]):
        best_score, best_ps_lst = float("-inf"), []
        temps_lst = []

        for ps in player_states:
            score = ps.calculate_score(temps_lst)
            if score > best_score:
                best_score, best_ps_lst = score, [ps]
            elif score == best_score:
                best_ps_lst.append(ps)

        if not best_ps_lst:
            print("bad!")
        return random.choice(best_ps_lst)





