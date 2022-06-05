import json
from typing import *
from exception import CityPlanException, my_assert
from helpers import *
from . import Criteria
from constants import VALID_POSNS

class CityPlan():
    def __init__(self, cp_dict: Dict) -> None:
        cp_keys = set(["criteria", "position", "score1", "score2"])
        my_assert(type(cp_dict) == dict and set(cp_dict.keys()) == cp_keys,
            CityPlanException,
            f"A city-plan must be a dictionary containing only these keys: {cp_keys}"
        )
        criteria, position, score1, score2 = cp_dict["criteria"], cp_dict["position"], cp_dict["score1"], cp_dict["score2"]

        self.position = position
        self.criteria = criteria
        self.score1 = score1
        self.score2 = score2

    @property 
    def criteria(self) -> Criteria:
        return self._criteria

    @criteria.setter
    def criteria(self, criteria: Union[List, str]) -> None:
        self._criteria = Criteria(criteria, self._position)
    
    @property
    def position(self) -> int:
        return self._position
    
    @position.setter
    def position(self, position: int) -> None:
        my_assert(check_type_and_membership(position, int, VALID_POSNS),
            CityPlanException,
            f"Given {position}, but city plan 'position' must be either 1, 2, or 3.")
        self._position = position

    @property
    def score1(self) -> int:
        return self._score1

    @score1.setter
    def score1(self, score1: int) -> None:
        my_assert(check_nat(score1),
            CityPlanException,
            f"Given {score1}, but city plan 'score1' must be a natural.")
        self._score1 = score1

    @property
    def score2(self) -> int:
        return self._score2

    @score2.setter
    def score2(self, score2: int) -> None:
        my_assert(check_nat(score2),
            CityPlanException,
            f"Given {score2}, but city plan 'score2' must be a natural.")
        self._score2 = score2

     
    def to_dict(self) -> Dict:
        '''
        Returns the Dictionary representation of a CityPlan.
        '''
        dict_repr = {
            "criteria": self._criteria.to_list_or_string(),
            "position": self._position,
            "score1": self._score1,
            "score2": self._score2
        }
        return dict_repr
    
    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a CityPlan.
        '''
        return json.dumps(self.to_dict())
    
    def __eq__(self, other: object) -> bool:
        return self.to_dict() == other.to_dict()
