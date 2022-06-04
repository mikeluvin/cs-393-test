import json
from typing import *
from helpers import *
from exception import HomeException, my_assert

class Home():
    def __init__(self, home_lst: List) -> None:
        my_assert(type(home_lst) == list and len(home_lst) == 4,
            HomeException,
            f"A home must be a list containing four elements.")
        
        fence_left, house, in_plan, fence_right = home_lst
        self.fence_left = fence_left
        self.fence_right = fence_right
        self.house = house
        self.in_plan = in_plan

    def _validate_house(self, house: Union[int, str, List]) -> Tuple[bool, Union[int, str], bool]:
        '''
        Returns valid_house, num, and bis.
        - valid_house is True if house satisfies one the following:
            1. natural, 0-17
            2. "blank"
            3. [natural, "bis"]
            4. "roundabout". Must have a fence on both sides in this case.
        - num: house number, a natural 0-17 or "blank"
        - bis: True if this house is a bis
        '''
        # if the house is a list, then it must be a bis: [natural, "bis"]
        if type(house) == list:
            if len(house) == 2 and (check_nat(house[0]) and house[0] <= 17 and house[1] == "bis"): 
                return True, house[0], True
        elif (check_nat(house) and house <= 17) or house == "blank":
            return True, house, False
        elif house == "roundabout":
            return (self._fence_left and self._fence_right), house, False

        return False, False, False    

    def _validate_used_ip(self, in_plan: bool) -> bool:
        '''
        Returns True if used-in-plan satisfies the following:
        1. boolean
        2. can only be True if the home has a number
        '''
        if type(in_plan) != bool:
            return False
        elif self._num in ["blank", "roundabout"] and in_plan is True:
            return False

        return True

    @property
    def fence_left(self) -> bool:
        return self._fence_left

    @fence_left.setter
    def fence_left(self, fence: bool) -> None:
        my_assert(type(fence) == bool,
            HomeException,
            f"Given {fence}, but fence-or-not must be a boolean.")
        self._fence_left = fence

    @property
    def fence_right(self) -> bool:
        return self._fence_right

    @fence_right.setter
    def fence_right(self, fence: bool) -> None:
        my_assert(type(fence) == bool,
            HomeException,
            f"Given {fence}, but fence-or-not must be a boolean.")
        self._fence_right = fence

    @property
    def house(self) -> Union[int, str, List]:
        '''
        Return the house, which is one of 
        1. natural, 0-17
        2. "blank"
        3. [natural, "bis"]
        4. "roundabout"
        '''
        return self._num if not self._is_bis else [self._num, "bis"]

    @house.setter
    def house(self, house: Union[int, str, List]):
        valid_house, num, bis = self._validate_house(house)
        my_assert(valid_house,
            HomeException,
            f"Given {house}, but house must be one of:\n1. natural, 0-17 \n2. 'blank'\n3. [natural, 'bis']\n4. 'roundabout' (with fences on both sides)")
        self.num, self.is_bis = num, bis

    @property
    def num(self) -> Union[int, str]:
        '''
        Return the house number; an integer 0 - 17, "blank", or "roundabout".
        '''
        return self._num

    @num.setter
    def num(self, num: Union[int, str]):
        my_assert((check_nat(num) and num <= 17) or num in ["blank", "roundabout"],
            HomeException,
            f"Given {num}, but house must either:\n1. natural, 0-17\n2. 'blank'\n3. 'roundabout'.")
        self._num = num

    @property
    def is_bis(self) -> bool:
        '''
        Return True if this home is a bis.
        '''
        return self._is_bis

    @is_bis.setter
    def is_bis(self, is_bis: bool) -> None:
        my_assert(type(is_bis) == bool,
            HomeException,
            f"Given {is_bis}, but bis must be a boolean.")
        self._is_bis = is_bis

    @property
    def in_plan(self) -> bool:
        '''
        Return True if this home is used in a city plan.
        '''
        return self._in_plan

    @in_plan.setter
    def in_plan(self, in_plan) -> None:
        my_assert(self._validate_used_ip(in_plan),
            HomeException,
            f"Given {in_plan}, but used-in-plan must be a boolean.")
        self._in_plan = in_plan

    def to_list(self) -> List:
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
            
