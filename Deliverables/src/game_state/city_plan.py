import json
from exception import *
from helpers import *
from constants import CRITERIA_CARDS, VALID_POSNS

class CityPlan():
    def __init__(self, cp_dict: dict) -> None:
        cp_keys = set(["criteria", "position", "score1", "score2"])
        if type(cp_dict) != dict or set(cp_dict.keys()) != cp_keys:
            raise CityPlanException(f"A city-plan must be a dictionary containing only these keys: {cp_keys}")
        criteria, position, score1, score2 = cp_dict["criteria"], cp_dict["position"], cp_dict["score1"], cp_dict["score2"]

        self.position = position
        self.criteria = criteria
        self.score1 = score1
        self.score2 = score2

    @property 
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, criteria: list) -> None:
        # criteria must be a list of naturals, or one of the special cases (below)
        is_incr_lst_ints = check_valid_lst(criteria, None, check_nat) and check_increasing(criteria)
        if not is_incr_lst_ints:
            # then check if it's one of the special cases
            if not (self.position < 3 and criteria in CRITERIA_CARDS[self.position-1]):
                raise CityPlanException(f"Given {criteria}, but city plan 'criteria' must be a list of \
                    integers or one of the specified criteria cards.")
        self._criteria = criteria
    
    @property
    def position(self) -> int:
        return self._position
    
    @position.setter
    def position(self, position) -> None:
        if not check_type_and_membership(position, int, VALID_POSNS):
            raise CityPlanException(f"Given {position}, but city plan 'position' must be either 1, 2, or 3.")
        self._position = position

    @property
    def score1(self) -> int:
        return self._score1

    @score1.setter
    def score1(self, score1) -> None:
        # scores must be naturals
        if not check_nat(score1):
            raise CityPlanException(f"Given {score1}, but city plan 'score1' must be a natural.")
        self._score1 = score1

    @property
    def score2(self) -> int:
        return self._score2

    @score2.setter
    def score2(self, score2) -> None:
        # scores must be naturals
        if not check_nat(score2):
            raise CityPlanException(f"Given {score2}, but city plan 'score2' must be a natural.")
        self._score2 = score2

     
    def to_dict(self) -> dict:
        '''
        Returns the Dictionary representation of a CityPlan.
        '''
        dict_repr = {
            "criteria": self._criteria,
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
