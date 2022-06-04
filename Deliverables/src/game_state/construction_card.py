import json
from typing import *
from constants import VALID_CC_NUMS
from exception import ConstructionCardException, my_assert
from helpers import *
from . import Effect

class ConstructionCard():
    def __init__ (self, cc_lst: List) -> None:
        my_assert(type(cc_lst) == list and len(cc_lst) == 2,
            ConstructionCardException,
            f"The input for construction-card must be [ int, string ]")

        num, effect = cc_lst
        self.num = num
        self.effect = effect

    @property
    def num(self) -> int:
        return self._num

    @num.setter
    def num(self, num: int) -> None:
        my_assert(check_type_and_membership(num, int, VALID_CC_NUMS),
            ConstructionCardException,
            f"Given {num}, but card numbers must be an integer between 1 and 15.")
        self._num = num

    @property
    def effect(self) -> Effect:
        return self._effect

    @effect.setter
    def effect(self, effect: str) -> None:
        self._effect = Effect(effect)

    def to_list(self) -> List:
        '''
        Returns the list representation of ConstructionCard, as outlined in the Assignment 3 spec.
        '''
        return [self._num, str(self._effect)]

    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a ConstructionCard.
        '''
        return json.dumps(self.to_list())

    def __eq__(self, other: object) -> bool:
        return self.to_list() == other.to_list()
