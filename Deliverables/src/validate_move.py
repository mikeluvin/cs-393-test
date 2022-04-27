from player_state import *
from game_state import *
from collections import defaultdict

class Change():
    def __init__(self) -> None:
        # if True, check that surveyor was used
        self.fences = False
        # check that the # on the house corresponds to the correct ConstructionCard
        # holds: [row, col, House object]
        self.houses = []
        # special case for bis
        self.bis_houses = []
        # if new houses used in plan, validate them with the GameState
        # holds: list of [row, col, House object]
        self.in_plan = []
        # check that landscaper card was used
        # holds row index of where park was built
        self.parks = None
        # check that pool card was used
        # holds [row, col] of pool that was added
        self.pools = []
        # check that temps card was used
        self.temps = False
        # check that a real estate agent was used
        self.agents = False
        # check that a refusal was used
        self.refusals = False
        # holds: list of [city_plan_idx, score_claimed]
        self.city_plan_score = []

    def is_effect_used(self) -> bool:
        '''
        Returns True if there was an effect used on this turn.
        '''
        return self.fences or self.bis_houses or self.parks or self.pools or self.temps or self.agents

    def is_city_plan_updated(self) -> bool:
        '''
        Returns True if there was an update to a city plan.
        '''
        return self.in_plan or self.city_plan_score
        
    def to_dict(self) -> dict:
        dict_repr = {
            "fences": self.fences,
            "houses": self.houses,
            "in_plan": self.in_plan,
            "parks": self.parks,
            "pools": self.pools,
            "temps": self.temps,
            "agents": self.agents,
            "refusals": self.refusals,
            "city_plan_score": self.city_plan_score
        }
        return dict_repr


def is_eq_or_mono_incr(f1: int, f2: int):
    '''
    Returns a boolean indicating if f1 = f2 or f1 + 1 = f2.
    '''
    return f1 == f2 or f1 + 1 == f2

def validate_move(game_state: GameState, ps1: PlayerState, ps2: PlayerState):
    '''
    Returns a boolean indicating whether the move from player_state_1 to
    player_state_2 is valid.
    - game_state: a GameState object
    - ps1: Initial PlayerState object
    - ps2: Subsequent PlayerState object
    '''

    # compare ps1 and ps2 to find the move
    # first, let's loop through the streets to find what # card was played
    # then loop through the construction cards to match with the card played 
    # if it's not a number in the construction cards set, see if the temps effect is in the effects set + has been used
    # if it is a number in the construction cards set, match its corresponding effects card
    change = Change()

    for i, s1 in enumerate(ps1.streets):
        s2 = ps2.streets[i]
        # loop through homes for each street
        for j, h1 in enumerate(s1.homes):
            h2 = s2.homes[j]
            prev_h1 = s1.homes[j-1] if j > 0 else None
            if not find_house_fence_in_plan(i, j, h1, h2, prev_h1, change):
                return False

        # determine if a park was built
        if not is_eq_or_mono_incr(s1.parks, s2.parks):
            return False
        elif s1.parks + 1 == s2.parks:
            # can only build one park per turn
            if change.parks is not None:
                return False
            change.parks = i

        # determine if a pool was built   
        for j, pool1 in enumerate(s1.pools):
            pool2 = s2.pools[j]
            if pool1 != pool2:
                # can't remove a pool, and can only build one pool per turn
                if pool1 or change.pools:
                    return False
                change.pools = [i, s2.get_pool_locs()[i][j]]

    to_check = [
        (ps1.temps, ps2.temps, "temps"),
        (ps1.refusals, ps2.refusals, "refusals"),
        (sum(ps1.agents), sum(ps2.agents), "agents")
        ]

    for f1, f2, ch_field in to_check:
        if not is_eq_or_mono_incr(f1, f2):
            return False
        elif f1 + 1 == f2:
            if ch_field == "temps":
                change.temps = True
            elif ch_field == "refusals":
                change.refusals = True
            elif ch_field == "agents":
                change.agents = True

    # find new city plan scores
    for i, cp1 in enumerate(ps1.city_plan_score):
        cp2 = ps2.city_plan_score[i]
        if cp1 != cp2:
            if cp1 != "blank":
                return False
            change.city_plan_score.append([i, cp2])

    #
    # now, we have all the changes from ps1 to ps2
    #
    # if a house wasn't built, then a refusal must've been used
    if not change.houses:
        # if a refusal wasn't used, an effect was used or city plan was updated,
        # then this move is invalid
        if not change.refusals or change.is_effect_used() or change.is_city_plan_updated():
            return False
        # otherwise, validate that the refusal was used correctly
        # try to place a house with each of the construction card values in each empty house
        return validate_refusal(ps1, game_state)    
    
    # if change.houses is True, then we can't have used a refusal
    if change.refusals:
        return False
        
    # otherwise, a card was played. validate card # used
    # it's possible that the house # matches more than one card. So, return
    # a list of possible cards
    poss_cards = validate_card_num(game_state, change)
    # if the house built doesn't correspond to any of the CCs, then move is invalid
    if poss_cards[0][1] == -1:
        return False
    
    # validate effect used
    for card_idx, card_num in poss_cards:
        effect_correct = validate_effect(game_state, change, card_idx)
        # if the effect used corresponds to this move, we're done
        if effect_correct:
            break

    # if the effect doesn't correspond to one of the possible cards, the move is invalid
    if not effect_correct:
        return False
    
    # validate city plan changes
    if not validate_used_in_plan(game_state, change):
        return False

    return True

def find_house_fence_in_plan(i:int, j:int, h1: Home, h2: Home, prev_h1: Home, change: Change):
    '''
    Determines if h2 is different from h1, and if so, what the changes were.
    Updates the Change object with the corresponding change.\n
    Returns False if there was an illegal move.
    '''
    if h1.num != h2.num:
        # make sure that h1 is blank. If not, return False
        if h1.num != "blank":
            return False

        if h2.is_bis:
            # can only have one new bis house
            if change.bis_houses:
                return False
            change.bis_houses = [i, j, h2]
        else:
            # can only have one new regular house
            if change.houses:
                return False
            # append the new house onto the Change list
            change.houses = [i, j, h2]
    
    if h1.fence_left != h2.fence_left:
        # if fence was removed, invalid. return False
        if h1.fence_left:
            return False
        # if we've already encountered a new fence, return False
        # since only one fence can be built per turn
        if change.fences:
            return False
        # if we try to build a fence between houses that are used
        # in a plan, that's invalid
        if prev_h1 and prev_h1.in_plan and h1.in_plan:
            return False
        change.fences = True

    if h1.in_plan != h2.in_plan:
        # if we try to remove from a plan, return False
        if h1.in_plan:
            return False
        change.in_plan.append([i, j, h2])

    return True

def validate_card_num(game_state: GameState, change: Change) -> tuple:
    '''
    Return the possible cards used, a list of [card_idx, card_num] values. 
    Returns [[-1, -1]] if the house placed doesn't correspond to any card.
    '''
    house_num = change.houses[2].num
    poss_cards = []
    for i, ccard in enumerate(game_state.ccards):
        if ccard.num == house_num:
            poss_cards.append((i, ccard.num))

    # if we get here, then maybe we used a temp
    for i, ccard in enumerate(game_state.ccards):
        possible_cards = set([ccard.num + x for x in range(-2, 3)])
        if house_num in possible_cards and game_state.effects[i] == "temp":
            # only possible that we used a temp if the field is marked True
            # in the Change object
            if change.temps:
                poss_cards.append((i, ccard.num))
    
    # if we get here, then we built an invalid house
    return poss_cards if poss_cards else [(-1, -1)]


def validate_effect(game_state: GameState, change: Change, card_idx: int) -> bool:
    '''
    Return True if the effect used (if any) corresponds to the card used.
    '''
    effect = game_state.effects[card_idx].effect
    effect_used = False
    bool_check = [
        (change.fences, "surveyor", lambda : False), 
        (change.bis_houses, "bis", lambda : False), 
        (change.agents, "agent", lambda : False), 
        (change.temps, "temp", lambda : False),
        # park must be built in the same row as the new house
        (change.parks is not None, "landscaper", lambda : change.houses[0] != change.parks),
        # pool must correspond to the new house
        (change.pools, "pool", lambda : change.houses[0] != change.pools[0] or change.houses[1] != change.pools[1])]

    for ch_field, curr_effect, extra_cond in bool_check:
        if ch_field:
            if effect == curr_effect and not effect_used:
                if extra_cond():
                    return False
                effect_used = True
            else:
                return False

    # if we get to this point where either:
    #   1. an effect was used correctly
    #   2. no effect was used
    # then, return True
    return True

def validate_refusal(ps1: PlayerState, game_state: GameState) -> bool:
    '''
    Return a boolean indicating whether playing a refusal is valid.
    '''
    for i in range(len(ps1.streets)):
        street = ps1.streets[i]
        for j in range(len(street.homes)):
            if street.homes[j].num == "blank":
                # try to play each of the construction cards
                for ccard in game_state.ccards:
                    street.homes[j].num = ccard.num
                    try:
                        # homes setter method needs the list representation of homes
                        # try setting homes with the new number
                        st_dict = street.to_dict()
                        street.homes = st_dict["homes"]
                    except StreetException:
                        # change home number back to "blank"
                        #
                        # *** something weird happened with the references, had to do this
                        # instead of h.num ***
                        #
                        street.homes[j].num = "blank"
                        st_dict = street.to_dict()
                        street.homes = st_dict["homes"]
                        continue
                    else:
                        # if we can successfully place a home, then the refusal is invalid
                        street.homes[j].num = "blank"
                        st_dict = street.to_dict()
                        street.homes = st_dict["homes"]
                        return False

    return True

def find_new_estates(change: Change):
    '''
    Returns a dictionary with the new estates claimed during this turn,
    or False if there was a rule violation.
    '''
    estates = defaultdict(int)
    first_home = True
    in_curr_estate = []
    for row, col, h in change.in_plan:
        if first_home:
            # first home MUST have a fence on the left, if not, it's invalid.
            if not h.fence_left:
                return False
            first_home = False
        else:
            # if not first home, then this home MUST be adjacent to the previous one
            if row != in_curr_estate[-1][0] or col != in_curr_estate[-1][1] + 1:
                return False

        in_curr_estate.append((row, col))

        if h.fence_right:
            # then, we found an estate
            estates[len(in_curr_estate)] += 1
            in_curr_estate = []
            first_home = True

    return estates
                    
def validate_used_in_plan(game_state: GameState, change: Change) -> bool:
    '''
    Returns a boolean indicating whether the new estates being used in
    a plan are valid.
    '''
    # first, find all new estates
    # keys are estate sizes, values are # of estates with that size
    estates = find_new_estates(change)
    if estates is False:
        return False

    # find city plans that were potentially claimed
    for i, cp_score in change.city_plan_score:
        # get city plan with "position" i+1
        cp_claimed = None
        for cp in game_state.city_plans:
            if cp.position == i + 1:
                cp_claimed = cp
                break

        # check that the score claimed by the player matches the score in the 
        # game state
        if game_state.city_plans_won[i]:
            if cp_score != cp_claimed.score2:
                return False
        else:
            if cp_score != cp_claimed.score1:
                return False

        # loop through estate size values in criteria and see
        # if there's estates matching those sizes
        for estate_size in cp_claimed.criteria:
            if estate_size in estates:
                estates[estate_size] -= 1
                # if there's no estates left with this size, remove 
                # it from the dictionary
                if estates[estate_size] == 0:
                    del estates[estate_size]
            else:
                # then, the player tried claiming the points for 
                # this city plan, but they don't have the correct estates
                return False

    # at this point, all the estates should be used. If there's any left,
    # it's invalid
    if len(estates) > 0:
        return False

    return True