import json
from state_helpers import *
from exception import *

class Home():
    def __init__(self, home_lst: list) -> None:
        if type(home_lst) != list or len(home_lst) != 4:
            raise HomeException(f"A home must be a list containing three elements.")
        
        fence_left, house, in_plan, fence_right = home_lst
        self.fence_left = fence_left
        self.fence_right = fence_right
        self.house = house
        self.in_plan = in_plan

    def _validate_house_and_bis(self, house):
        '''
        Returns valid_house, num, and bis.
        - valid_house is True if house satisfies one the following:
            1. natural, 0-17
            2. "blank"
            3. [natural, "bis"]
        - num: house number, a natural 0-17 or "blank"
        - bis: True if this house is a bis
        '''
        # if the house is a list, then it must be a bis: [natural, "bis"]
        if type(house) == list:
            if len(house) == 2 and (check_nat(house[0]) and house[0] <= 17 and house[1] == "bis"): 
                return True, house[0], True
        # if the house is a natural
        elif check_nat(house) and house <= 17:
            return True, house, False
        # if the house is "blank"
        elif house == "blank":
            return True, "blank", False

        return False, False, False    

    def _validate_used_ip(self, in_plan: bool) -> bool:
        '''
        Returns True if used-in-plan satisfies the following:
        1. boolean
        2. can only be True if the home has a number
        '''
        if type(in_plan) != bool:
            return False
        elif self._num == "blank" and in_plan is True:
            return False

        return True

    @property
    def fence_left(self) -> bool:
        return self._fence_left

    @fence_left.setter
    def fence_left(self, fence) -> None:
        if type(fence) != bool:
            raise HomeException(f"Given {fence}, but fence-or-not must be a boolean.")
        self._fence_left = fence

    @property
    def fence_right(self) -> bool:
        return self._fence_right

    @fence_right.setter
    def fence_right(self, fence) -> None:
        if type(fence) != bool:
            raise HomeException(f"Given {fence}, but fence-or-not must be a boolean.")
        self._fence_right = fence

    @property
    def house(self):
        '''
        Return the house, which is one of 
        1. natural, 0-17
        2. "blank"
        3. [natural, "bis"]
        '''
        return self._num if not self._is_bis else [self._num, "bis"]

    @house.setter
    def house(self, house):
        valid_house, num, bis = self._validate_house_and_bis(house)
        if not valid_house:
            raise HomeException(f"Given {house}, but house must be one of:\n1. natural, 0-17\n2. 'blank'\n3. [natural, 'bis']")
        self._num, self._is_bis = num, bis

    @property
    def num(self):
        '''
        Return the house number; an integer 0 - 17, or "blank".
        '''
        return self._num

    @num.setter
    def num(self, num):
        if (check_nat(num) and num <= 17) or num == "blank":
            self._num = num
        else:
            raise HomeException(f"Given {num}, but house must either:\n1. natural, 0-17\n2. 'blank'.")

    @property
    def is_bis(self) -> bool:
        '''
        Return True if this home is a bis.
        '''
        return self._is_bis

    @property
    def in_plan(self) -> bool:
        '''
        Return True if this home is used in a city plan.
        '''
        return self._in_plan

    @in_plan.setter
    def in_plan(self, in_plan) -> None:
        if not self._validate_used_ip(in_plan):
            raise HomeException(f"Given {in_plan}, but used-in-plan must be a boolean.")
        self._in_plan = in_plan

    def to_list(self) -> list:
        '''
        Returns the list representation of a home.
        '''
        return [self._fence_left, self._num if not self._is_bis else [self._num, "bis"], self._in_plan]

    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a home.
        '''
        return json.dumps(self.to_list())

    def __eq__(self, other: object) -> bool:
        return self.to_list() == other.to_list()
            

class Street():
    def __init__(self, st_dict: dict, st_idx: int) -> None:
        # index of this street
        self._idx = st_idx
        # number of parks in each street
        self._parks_maxes = [3, 4, 5]
        # pool locations for each street
        self._pool_locs = [[2, 6, 7], [0, 3, 7], [1, 6, 10]]
        st_keys = set(["homes", "parks", "pools"])
        if type(st_dict) != dict or set(st_dict.keys()) != st_keys:
            raise StreetException(f"A street must be a dictionary containing only these keys: {st_keys}")

        homes, parks, pools = st_dict["homes"], st_dict["parks"], st_dict["pools"]
        self.pools = pools
        self.homes = homes
        # validate homes: strictly increasing (except for bis)  DONE
        # bis must be the same number as an adjacent house  DONE
        # house #s must be between 0 and 17     DONE
        # bis cannot have a pool    DONE
        # bis can't be separated from its duplicate by a fence  DONE
        self.parks = parks
        # need to check that # of parks is <= # of non-bis houses on this street    DONE
        # need to check that a house has a number to be used in a housing estate plan   DONE (inside Home class)
        # need to check that # of pools <= # houses in row  DONE

    @property 
    def homes(self):
        return self._homes

    @homes.setter
    def homes(self, homes: list) -> None:
        if not self._validate_homes(homes):
            raise ValueError(f"homes for row {self._idx+1} must be a list with {10 + self._idx} homes.")
        self._build_homes(homes)
        self._check_homes_rule_violations()

    @property
    def pools(self):
        return self._pools

    @pools.setter
    def pools(self, pools: list) -> None:
        if not check_valid_lst(pools, 3, lambda x: type(x) == bool):
            raise StreetException(f"Given {pools}, but pools must be a list of 3 boolean values")
        self._pools = pools

    @property
    def parks(self) -> int:
        return self._parks

    @parks.setter
    def parks(self, parks: list) -> None:
        if not self._validate_parks(parks):
            raise StreetException(f"Given {parks}, but parks must be a natural no greater than {self._parks_maxes[self._idx]}.")
        self._parks = parks

    def get_pool_locs(self):
        return self._pool_locs

    def _build_homes(self, homes: list) -> None:
        '''
        Initialize a list of our internal representation of homes, the Home class.
        NOTE: we represent the first home just like the rest, as a list of three fields.
        The "fence-or-not" flag is always False for it.
        '''
        home_lst = []
        curr_home = [True]
        for i in range(len(homes)):
            if i == 0:
                curr_home.append(homes[i])
                continue
            elif i == 1:
                curr_home.append(homes[i])
                # add on the left fence of the next house
                curr_home.append(homes[i+1][0])
            elif i == len(homes) - 1:
                curr_home = homes[i]
                curr_home.append(True)
            else:
                curr_home = homes[i]
                curr_home.append(homes[i+1][0])

            home_lst.append(curr_home)

        self._homes = [Home(home) for home in home_lst]       
            

    def _validate_homes(self, homes: list) -> bool:
        '''
        Returns True if homes is the correct length and formatted as
        [ house, used-in-plan, [ fence-or-not, house, used-in-plan ], ... ].
        '''
        lengths = [11, 12, 13]
        valid_len = lengths[self._idx]
        return type(homes) == list and len(homes) == valid_len and check_valid_lst(homes[2:], valid_len - 2, lambda x : type(x) == list)

    def _check_homes_rule_violations(self) -> None:
        '''
        Check that the homes don't violate any game rules.
        '''
        self._check_homes_increasing_and_bis()
        self._check_homes_pools()
    
    def _check_homes_increasing_and_bis(self) -> None:
        '''
        Check that: 
        - homes are strictly increasing (except for bis houses)
        - bis houses are the same number as an adjacent house
        - bis houses are not separated by fences 
        - house from which bis originates is not also a bis
        '''
        prev_non_bis = -1
        self._non_bis_ct = 0
        for i, home in enumerate(self._homes):
            next_home = self._homes[i+1] if i < len(self._homes) - 1 else None
            prev_home = self._homes[i-1] if i > 0 else None
            curr_num = home.num

            if home.is_bis:
                if next_home and curr_num == next_home.num and not next_home.fence_left:
                    continue
                if prev_home and curr_num == prev_home.num and not home.fence_left:
                    continue
                raise StreetException(f"Violation in street {self._idx + 1}: bis must have the same number as an adjacent house.")
            else:
                if curr_num == "blank":
                    continue
                
                self._non_bis_ct += 1
                if curr_num > prev_non_bis:
                    prev_non_bis = curr_num
                else:
                    raise StreetException(f"Violation in street {self._idx + 1}: non-bis house numbers must be strictly increasing.")
                
    def _check_homes_pools(self) -> None:
        '''
        Check that a house with a pool:
        1. isn't blank
        2. isn't bis
        '''
        curr_pool_locs = self._pool_locs[self._idx]
        for i, has_pool in enumerate(self._pools):
            if has_pool:
                home = self._homes[curr_pool_locs[i]]
                if home.num == "blank" or home.is_bis:
                    raise StreetException(f"Violation in street {self._idx + 1}: pool cannot be on a bis or blank house.")


    def _validate_parks(self, parks: int) -> bool:
        '''
        Returns True if the following are True:
        1. parks is a natural
        2. parks is <= the max value for its street
        3. parks is <= the number of houses filled on this street
        '''
        return check_nat(parks) and parks <= self._parks_maxes[self._idx] and parks <= self._non_bis_ct

    def to_dict(self) -> dict:
        # convert the first home back to the initial representation
        first_home = self._homes[0].to_list()
        homes_lst = [first_home[1], first_home[2]]
        homes_lst.extend([h.to_list() for h in self._homes[1:]])
        dict_repr = {
            "homes": homes_lst,
            "parks": self._parks,
            "pools": self._pools
        }
        return dict_repr

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def __eq__(self, other: object) -> bool:
        return self.to_dict() == other.to_dict()



class PlayerState():
    def __init__(self, ps_dict: dict) -> None:
        # max number of cross-outs for each agent
        self._agent_maxes = [1, 2, 3, 4, 4, 4]
        ps_keys = set(["agents", "city-plan-score", "refusals", "streets", "temps"])
        if type(ps_dict) != dict or set(ps_dict.keys()) != ps_keys:
            raise PlayerStateException(f"A player-state must be a dictionary containing only these keys: {ps_keys}")

        agents, cp_scores, refusals = ps_dict["agents"], ps_dict["city-plan-score"], ps_dict["refusals"]
        streets, temps = ps_dict["streets"], ps_dict["temps"]

        self.agents = agents
        self.city_plan_score = cp_scores
        self.refusals = refusals
        self.streets = streets
        self.temps = temps

    def _validate_agents(self, agents: list) -> bool:
        '''
        Returns True if the following are True:
        1. agents is a list of 6 naturals
        2. each element is within its respective maximum value.
        '''
        return check_valid_lst(agents, 6, check_nat) and all(a <= self._agent_maxes[i] for i, a in enumerate(agents))

    @property
    def streets(self) -> list:
        '''
        Returns the list of Street objects for this PlayerState.
        '''
        return self._streets

    @streets.setter
    def streets(self, streets) -> None:
        if not check_valid_lst(streets, 3, lambda x: type(x) == dict):
            raise PlayerStateException(f"Given {streets}, but streets must be a list 3 dictionaries.")
        self._streets = [Street(st, i) for i, st in enumerate(streets)]

    @property
    def agents(self):
        '''
        Returns the list of agents for this PlayerState.
        '''
        return self._agents

    @agents.setter
    def agents(self, agents: list) -> None:
        if not self._validate_agents(agents):
            raise PlayerStateException(f"Given {agents}, but agents must be a list of 6 naturals.")
        self._agents = agents

    @property
    def city_plan_score(self):
        return self._cp_scores

    @city_plan_score.setter
    def city_plan_score(self, cp_scores: list):
        if not check_valid_lst(cp_scores, 3, lambda x: (check_nat(x) or x == "blank")):
            raise PlayerStateException(f"Given {cp_scores}, but city_plan_scores must be a list containing naturals or 'blank'.")
        self._cp_scores = cp_scores
    
    @property
    def refusals(self) -> int:
        return self._refusals

    @refusals.setter
    def refusals(self, refusals) -> None:
        if not check_nat(refusals) or refusals > 3:
            raise PlayerStateException(f"Given {refusals}, but refusals must be either 0, 1, 2, or 3.")
        self._refusals = refusals

    @property
    def temps(self) -> int:
        return self._temps

    @temps.setter
    def temps(self, temps) -> None:
        if not check_nat(temps) or temps > 11:
            raise PlayerStateException(f"Given {temps}, but temps must be an integer between 0 and 11.")
        self._temps = temps
        
    def to_dict(self) -> dict:
        '''
        Returns the Dictionary representation of a PlayerState.
        '''
        dict_repr = {
            "agents": self._agents,
            "city-plan-score": self._cp_scores,
            "refusals": self._refusals,
            "streets": [street.to_dict() for street in self._streets],
            "temps": self._temps
        }

        return dict_repr
    
    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a PlayerState.
        '''
        return json.dumps(self.to_dict())

    def __eq__(self, other: object) -> bool:
        return self.to_dict() == other.to_dict()

