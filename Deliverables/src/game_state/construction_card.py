import json
from exception import *
from helpers import *
from . import Effect

class ConstructionCard():
    def __init__ (self, cc_lst: list) -> None:
        if type(cc_lst) != list or len(cc_lst) != 2:
            raise ConstructionCardException(f"The input for construction-card must be [ int, string ]")

        num, effect = cc_lst
        # valid range of card number is 1-15
        self._valid_range = set(range(1, 16))
        self.num = num
        self.effect = effect

    @property
    def num(self) -> int:
        return self._num

    @num.setter
    def num(self, num) -> None:
        # validate class inputs based on game spec
        if not check_type_and_membership(num, int, self._valid_range):
            raise ConstructionCardException(f"Given {num}, but card numbers must be an integer between 1 and 15.")
        self._num = num

    @property
    def effect(self) -> Effect:
        return self._effect

    @effect.setter
    def effect(self, effect) -> None:
        self._effect = Effect(effect)

    def to_list(self) -> list:
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
