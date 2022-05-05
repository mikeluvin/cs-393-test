import json
from helpers import *
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
        self.num, self.is_bis = num, bis

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

    @is_bis.setter
    def is_bis(self, is_bis: bool) -> None:
        if type(is_bis) != bool:
            raise HomeException(f"Given {is_bis}, but bis must be a boolean.")
        self._is_bis = is_bis

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
            
