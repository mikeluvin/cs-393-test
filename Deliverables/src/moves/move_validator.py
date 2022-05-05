from player_state import *
from game_state import *
from exception import MoveException
from collections import defaultdict
from helpers import is_eq_or_mono_incr

class MoveValidator():
    def __init__(self, game_state: GameState, ps1: PlayerState, ps2: PlayerState) -> None:
        '''
        - game_state: a GameState object
        - ps1: Initial PlayerState object
        - ps2: Subsequent PlayerState object
        '''
        self._game_st = game_state
        self._ps1 = ps1
        self._ps2 = ps2
        # if True, check that surveyor was used
        self._fences = False
        # check that the # on the house corresponds to the correct ConstructionCard
        # holds: [row, col, House object]
        self._houses = []
        # special case for bis
        self._bis_houses = []
        # if new houses used in plan, validate them with the GameState
        # holds: list of [row, col, House object]
        self._in_plan = []
        # check that landscaper card was used
        # holds row index of where park was built
        self._parks = None
        # check that pool card was used
        # holds [row, col] of pool that was added
        self._pools = []
        # check that temps card was used
        self._temps = False
        # check that a real estate agent was used
        self._agents = False
        # check that a refusal was used
        self._refusals = False
        # holds: list of [city_plan_idx, score_claimed]
        self._city_plan_score = []

    def is_effect_used(self) -> bool:
        '''
        Returns True if there was an effect used on this turn.
        '''
        return self._fences or self._bis_houses or self._parks or self._pools or self._temps or self._agents

    def is_city_plan_updated(self) -> bool:
        '''
        Returns True if there was an update to a city plan.
        '''
        return self._in_plan or self._city_plan_score
        
    def to_dict(self) -> dict:
        dict_repr = {
            "fences": self._fences,
            "houses": self._houses,
            "in_plan": self._in_plan,
            "parks": self._parks,
            "pools": self._pools,
            "temps": self._temps,
            "agents": self._agents,
            "refusals": self._refusals,
            "city_plan_score": self._city_plan_score
        }
        return dict_repr

    def validate_move(self):
        '''
        Validates the move from player_state_1 to player_state_2.\n
        Raises a MoveException otherwise.
        '''
        self._find_street_related_changes()
        self._find_rest_of_changes()

        # now, we have all the changes from ps1 to ps2
        #
        # if a house wasn't built, then a refusal must've been used
        if self._validate_refusal_or_not() is True:
            return
            
        # otherwise, a card was played. validate card # used
        # it's possible that the house # matches more than one card. So, return
        # a list of possible cards
        poss_cards = self._validate_card_num()
        # validate effect used with the possible cards
        self._validate_effect(poss_cards)
        # validate city plan changes
        self._validate_used_in_plan()

    def _find_street_related_changes(self):
        '''
        Validates the changes in the streets.
        These fields are: new home(s), parks, and pools.\n
        If valid, populates the changes in the their respective member variables.
        Raises a MoveException otherwise.
        '''
        for i, s1 in enumerate(self._ps1.streets):
            s2 = self._ps2.streets[i]
            # loop through homes for each street
            for j, h1 in enumerate(s1.homes):
                h2 = s2.homes[j]
                prev_h1 = s1.homes[j-1] if j > 0 else None
                self._find_house_fence_in_plan(i, j, h1, h2, prev_h1)

            # determine if a park was built
            if not is_eq_or_mono_incr(s1.parks, s2.parks):
                raise MoveException(f'Parks must stay the same or increase by only one.')
            elif s1.parks + 1 == s2.parks:
                if (self._parks is not None or 
                    not self._houses or self._houses[0] != i):
                    raise MoveException(f'Can only build one park per turn, and it must be \
                             in the same row as the new house.')
                self._parks = i

            # determine if a pool was built   
            for j, pool1 in enumerate(s1.pools):
                pool2 = s2.pools[j]
                if pool1 != pool2:
                    if (pool1 or self._pools or 
                        not self._houses or 
                        self._houses[0] != i or self._houses[1] != s2.get_pool_locs()[i][j]):
                        raise MoveException(f'Cannot remove a pool, and can only build one pool \
                             in the new house you placed.')
                    self._pools = [i, s2.get_pool_locs()[i][j]]

    def _find_rest_of_changes(self):
        '''
        Validates the changes in temps, refusals, agents, and city plan scores.\n
        If valid, populates the changes in the their respective member variables.
        Raises a MoveException otherwise.
        '''
        to_check = [
            (self._ps1.temps, self._ps2.temps, "temps"),
            (self._ps1.refusals, self._ps2.refusals, "refusals"),
            (sum(self._ps1.agents), sum(self._ps2.agents), "agents")
            ]

        for f1, f2, ch_field in to_check:
            if not is_eq_or_mono_incr(f1, f2):
                raise MoveException(f'{ch_field} must stay the same or increase by only one.')
            elif f1 + 1 == f2:
                if ch_field == "temps":
                    self._temps = True
                elif ch_field == "refusals":
                    self._refusals = True
                elif ch_field == "agents":
                    self._agents = True

        # find new city plan scores
        for i, cp1 in enumerate(self._ps1.city_plan_score):
            cp2 = self._ps2.city_plan_score[i]
            if cp1 != cp2:
                if cp1 != "blank":
                    raise MoveException(f"You can only claim a city plan once.")
                self._city_plan_score.append([i, cp2])

    def _find_house_fence_in_plan(self, i:int, j:int, h1: Home, h2: Home, prev_h1: Home):
        '''
        Determines if h2 is different from h1, and if so, what the changes were.
        Updates the member variables with the corresponding change.\n
        Returns False if there was an illegal move.
        '''
        if h1.num != h2.num:
            if h1.num != "blank":
                raise MoveException(f"Cannot change the number on a house after it's built.")

            if h2.is_bis:
                if self._bis_houses:
                    raise MoveException(f"You may only build one BIS house per turn.")
                self._bis_houses = [i, j, h2]
            else:
                if self._houses:
                    raise MoveException(f"You may only build one non-BIS house per turn.")
                # append the new house onto the Change list
                self._houses = [i, j, h2]
        
        if h1.fence_left != h2.fence_left:
            if h1.fence_left:
                raise MoveException(f"Cannot remove a fence from a house.")
            if self._fences:
                raise MoveException(f"Cannot build more than one fence per turn.")
            if prev_h1 and prev_h1.in_plan and h1.in_plan:
                raise MoveException(f"Cannot build a fence between houses marked used-in-plan.")
            self._fences = True

        if h1.in_plan != h2.in_plan:

            if h1.in_plan:
                raise MoveException(f"Cannot remove a house from a city plan.")
            self._in_plan.append([i, j, h2])

    def _validate_card_num(self) -> tuple:
        '''
        Return the possible cards used, a list of [card_idx, card_num] values. 
        Returns [[-1, -1]] if the house placed doesn't correspond to any card.
        '''
        house_num = self._houses[2].num
        poss_cards = []
        for i, ccard in enumerate(self._game_st.ccards):
            if ccard.num == house_num:
                poss_cards.append((i, ccard.num))

        # if a temp was (supposedly) used, check to see if there's a corresponding
        # card 
        if self._temps:
            for i, ccard in enumerate(self._game_st.ccards):
                possible_cards = set([max(ccard.num + x, 0) for x in range(-2, 3)])
                if house_num in possible_cards and self._game_st.effects[i] == "temp":
                    poss_cards.append((i, ccard.num))

        if not poss_cards:
            raise MoveException(f"You must play a card.")
        
        return poss_cards

    def _validate_effect(self, poss_cards: list):
        '''
        Validates that the effect used corresponds to one of the possible cards played.
        Raises a MoveException otherwise.
        '''
        effect_used = None
        effects_lst = [
            (self._fences, "surveyor"), 
            (self._bis_houses, "bis"), 
            (self._agents, "agent"), 
            (self._temps, "temp"),
            (self._parks is not None, "landscaper"),
            (self._pools, "pool")]

        for ch_field, curr_effect in effects_lst:
            if ch_field:
                if effect_used is not None:
                    raise MoveException(f"Cannot use multiple effects.")
                effect_used = curr_effect

        poss_effects = [self._game_st.effects[i].effect for i, _ in poss_cards]
        if effect_used is not None and effect_used not in poss_effects:
            raise MoveException(f"Invalid use of {effect_used} effect.")
        # if we get to this point, either:
        #   1. an effect was used correctly
        #   2. no effect was used 

    def _validate_refusal_or_not(self):
        '''
        Validates that the use of a refusal (or lack thereof) is valid.\n
        Returns True if a refusal was succesfully played, None if there was no attempt at a refusal.
        Raises a MoveException otherwise.
        '''
        if not self._houses:
            if not self._refusals:
                raise MoveException(f"Must either place a house or use a refusal.")
            if self.is_effect_used() or self.is_city_plan_updated():
                raise MoveException(f"Cannot use a refusal and an (effect or a city plan).")
            return self._can_player_place_home()
        elif self._refusals:
            raise MoveException(f"Cannot use refusal and place a house.")

    def _can_player_place_home(self) -> bool:
        for i in range(len(self._ps1.streets)):
            street = self._ps1.streets[i]
            for j in range(len(street.homes)):
                if street.homes[j].num == "blank":
                    # try to play each of the construction cards
                    for ccard in self._game_st.ccards:
                        try:
                            # try setting home with the new number
                            street.try_place_new_home(j, ccard.num)
                        except StreetException:
                            # change home number back to "blank"
                            street.try_place_new_home(j, "blank")
                        else:
                            # if we can successfully place a home, then the refusal is invalid
                            street.try_place_new_home(j, "blank")
                            raise MoveException(f"Invalid refusal use, you can place a house.")
        return True

    def _find_new_estates(self):
        '''
        Returns a dictionary with the new estates claimed during this turn,
        or False if there was a rule violation. Keys are estate sizes, values are # of estates with that size
        '''
        estates = defaultdict(int)
        first_home = True
        in_curr_estate = []
        for row, col, h in self._in_plan:
            if first_home:
                # first home MUST have a fence on the left, if not, it's invalid.
                if not h.fence_left:
                    raise MoveException(f"City plans must be enclosed by fences.")
                first_home = False
            else:
                # if not first home, then this home MUST be adjacent to the previous one
                if row != in_curr_estate[-1][0] or col != in_curr_estate[-1][1] + 1:
                    raise MoveException(f"Houses used in the same city plan estate must be adjacent.")

            in_curr_estate.append((row, col))

            if h.fence_right:
                # then, we found an estate
                estates[len(in_curr_estate)] += 1
                in_curr_estate = []
                first_home = True

        return estates
                        
    def _validate_used_in_plan(self) -> bool:
        '''
        Validates the new estates being used in a plan. Returns a MoveException
        otherwise.
        '''
        # first, find all new estates
        # keys are estate sizes, values are # of estates with that size
        estates = self._find_new_estates()

        # find city plans that were potentially claimed
        for i, cp_score in self._city_plan_score:
            # get city plan with "position" i+1
            cp_claimed = None
            for cp in self._game_st.city_plans:
                if cp.position == i + 1:
                    cp_claimed = cp
                    break

            if self._game_st.city_plans_won[i]:
                if cp_score != cp_claimed.score2:
                    raise MoveException(f"City plan score invalid.")
            else:
                if cp_score != cp_claimed.score1:
                    raise MoveException(f"City plan score invalid.")

            # loop through estate size values in criteria and see
            # if there's estates matching those sizes
            for estate_size in cp_claimed.criteria:
                if estate_size in estates:
                    estates[estate_size] -= 1
                    if estates[estate_size] == 0:
                        del estates[estate_size]
                else:
                    # then, the player tried claiming the points for 
                    # this city plan, but they don't have the correct estates
                    raise MoveException(f"Invalid claim of city plan with criteria {cp_claimed.criteria}.")

        # at this point, all the estates should be used. If there's any left,
        # it's invalid
        if len(estates) > 0:
            raise MoveException(f"Marked more city plan estates than is allowed.")

