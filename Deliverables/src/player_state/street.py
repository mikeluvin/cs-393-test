import json
from helpers import *
from exception import StreetException
from . import Home
from constants import PARK_MAXES, POOL_LOCS
from collections import defaultdict

class Street():
    def __init__(self, st_dict: dict, st_idx: int) -> None:
        # index of this street
        self._idx = st_idx
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
            raise StreetException(f"homes for row {self._idx+1} must be a list with {10 + self._idx} homes.")
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
        # count number of non-bis houses
        non_bis_ct = [type(h.num) == int and not h.is_bis for h in self._homes].count(True)
        if not self._validate_parks(parks, non_bis_ct):
            raise StreetException(f"Given {parks}, but parks must be a natural no greater than {min(non_bis_ct, PARK_MAXES[self._idx])}.")
        self._parks = parks

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
                # making a copy so we don't modify the input json (for testing purposes)
                curr_home = homes[i].copy()
                curr_home.append(True)
            else:
                curr_home = homes[i].copy()
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
        self._check_homes_increasing()
        self._check_homes_bis()
        self._check_homes_pools()

    def _check_homes_increasing(self) -> None:
        '''
        Check that homes are increasing. Accounts for roundabouts.
        '''
        prev_non_bis = -1
        for home in self._homes:
            if home.is_bis or home.num == "blank":
                continue
            if home.num == "roundabout":
                prev_non_bis = -1
                continue
            if home.num <= prev_non_bis:
                raise StreetException(f"Violation in street {self._idx + 1}: non-bis house numbers must be strictly increasing.")
            
            prev_non_bis = home.num
    
    def _check_homes_bis(self) -> None:
        '''
        Check that: 
        - bis houses are the same number as an adjacent house
        - bis houses are not separated by fences 
        - bis house(s) have a non-bis origin house
        '''
        # bis_anchor: the "anchor" non-bis house, which is located to the left
        # of the bis house(s). 
        # bis_anchor is None if there's no anchor, the house number otherwise
        #
        # bis_obligation: the bis house number that doesn't yet have an anchor.
        # Therefore, the first non-bis house to the right of the bis house(s)
        # must fill this obligation (by being the same number). 
        # bis_obligation is None if there's no outstanding obligation, the
        # house number otherwise.
        bis_anchor, bis_obligation = None, None
        for i, home in enumerate(self._homes):
            next_home = self._homes[i+1] if i < len(self._homes) - 1 else None
            prev_home = self._homes[i-1] if i > 0 else None
            curr_num = home.num

            if home.is_bis:
                if bis_anchor != curr_num:
                    bis_obligation = curr_num

                if prev_home and curr_num == prev_home.num and not home.fence_left:
                    continue
                if next_home and curr_num == next_home.num and not home.fence_right:
                    continue

                raise StreetException(f"Violation in street {self._idx + 1}: bis must have the same number as an adjacent house.")
            else:
                if bis_obligation is not None and curr_num != bis_obligation:
                    raise StreetException(f"Violation in street {self._idx + 1}: bis played next to a house with a different number (or blank).")
                if curr_num == "blank":
                    bis_anchor, bis_obligation = None, None
                    continue

                bis_anchor, bis_obligation = curr_num, None
                    
        # if we make it outside the loop but still fulfilled the bis_obligation, it's invalid
        if bis_obligation is not None:
            raise StreetException(f"Violation in street {self._idx + 1}: bis played next to a house with a different number (or blank).")
                
    def _check_homes_pools(self) -> None:
        '''
        Check that a house with a pool isn't a blank, bis, or roundabout
        '''
        curr_pool_locs = POOL_LOCS[self._idx]
        for i, has_pool in enumerate(self._pools):
            if has_pool:
                home = self._homes[curr_pool_locs[i]]
                if type(home.num) != int or home.is_bis:
                    raise StreetException(f"Violation in street {self._idx + 1}: pool cannot be on a blank, bis, or roundabout house.")


    def _validate_parks(self, parks: int, non_bis_ct: int) -> bool:
        '''
        Returns True if the following are True:
        1. parks is a natural
        2. parks is <= the max value for its street
        3. parks is <= the number of non-bis houses filled on this street
        '''
        return check_nat(parks) and parks <= PARK_MAXES[self._idx] and parks <= non_bis_ct
    
    def try_place_new_home(self, home_idx: int, new_num) -> None:
        '''
        Place a new home with new_num at index home_idx and validate that it doesn't
        break any rules.
        '''
        self.homes[home_idx].num = new_num
        self._check_homes_rule_violations()

    def parks_score(self) -> int:
        # (mex number of parks)* 4 - 2 = max score
        return self._parks * 2 if self._parks != PARK_MAXES[self._idx] else self._parks * 4 - 2

    def pools_built(self) -> int:
        return self._pools.count(True)
    
    def estates_dict(self) -> dict:
        ret_dict = defaultdict(int)
        in_estate = False
        size_counter = 0
        for home in self._homes:
            if home.num != "blank":
                if home._fence_left:
                    in_estate = True
                if in_estate:
                    size_counter += 1
                    if size_counter > 6:
                        size_counter = 0
                        in_estate = False
                        continue
                    if home._fence_right:
                        ret_dict[size_counter] += 1
                        size_counter = 0
                        in_estate = False
            else:
                size_counter = 0
                in_estate = False
        
        return ret_dict

    def bis_count(self) -> int:
        return [h.is_bis for h in self._homes].count(True)

    def roundabout_count(self) -> int:
        return [h.num == "roundabout" for h in self._homes].count(True)

    def is_full(self) -> bool:
        return all([h.num != "blank" for h in self._homes])

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

