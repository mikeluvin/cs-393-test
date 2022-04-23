import json
from exception import *
from state_helpers import *


class Effect():
    def __init__(self, effect: str) -> None:
        self._effects = set(["surveyor", "agent", "landscaper", "pool", "temp", "bis"])
        self.effect = effect

    @property
    def effect(self) -> str:
        return self._effect

    @effect.setter
    def effect(self, effect: str) -> None:
        if not check_type_and_membership(effect, str, self._effects):
            raise EffectException(f"Given {effect}, but effect must be one of {self._effects}.")
        self._effect = effect

    def __repr__(self) -> str:
        return self._effect

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

class CityPlan():
    def __init__(self, cp_dict: dict) -> None:
        cp_keys = set(["criteria", "position", "score1", "score2"])
        if type(cp_dict) != dict or set(cp_dict.keys()) != cp_keys:
            raise CityPlanException(f"A city-plan must be a dictionary containing only these keys: {cp_keys}")
        criteria, position, score1, score2 = cp_dict["criteria"], cp_dict["position"], cp_dict["score1"], cp_dict["score2"]

        # valid city plan positions are 1, 2, or 3
        self._valid_posns = set(range(1, 4))
        self.criteria = criteria
        self.position = position
        self.score1 = score1
        self.score2 = score2

    @property 
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, criteria: list) -> None:
        # criteria must be a list of naturals
        if not check_valid_lst(criteria, None, check_nat) or not check_increasing(criteria):
            raise CityPlanException(f"Given {criteria}, but city plan 'criteria' must be a list of integers.")
        self._criteria = criteria
    
    @property
    def position(self) -> int:
        return self._position
    
    @position.setter
    def position(self, position) -> None:
        if not check_type_and_membership(position, int, self._valid_posns):
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


class GameState():
    def __init__(self, gs_dict: dict) -> None:
        gs_keys = set(["city-plans", "city-plans-won", "construction-cards", "effects"])
        if type(gs_dict) != dict or set(gs_dict.keys()) != gs_keys:
            raise GameStateException(f"A game-state must be a dictionary containing only these keys: {gs_keys}")

        city_plans, city_plans_won = gs_dict["city-plans"], gs_dict["city-plans-won"]
        construct_cards, effects = gs_dict["construction-cards"], gs_dict["effects"]

        self.city_plans = city_plans
        self.city_plans_won = city_plans_won
        self.ccards = construct_cards
        self.effects = effects
        
    # the city_plans_won, construction_cards, and effects fields are all updated as the game progresses
    # while not necessary for this assignment, in the future we may use the 'property' decorator
    # (see https://docs.python.org/3/library/functions.html#property)
    # to make for an easier getter/setter API and to enforce the field constraints.
    
    @property
    def city_plans(self):
        """The 'city_plans' field, a list of length 3 containing CityPlan objects."""
        return self._city_plans

    @city_plans.setter
    def city_plans(self, city_plans):
        if not check_valid_lst(city_plans, 3, lambda x: type(x) == dict):
            raise GameStateException(f"Given {city_plans}, but city_plans must be a list of 3 dictionaries.")

        cp_posns = set([cp.get("position", -1) for cp in city_plans])
        if cp_posns != set([1, 2, 3]):
            raise GameStateException(f"The list of city-plans must have three plans with unique positions 1, 2, and 3.")
        self._city_plans = [CityPlan(cp) for cp in city_plans]
    
    @property
    def city_plans_won(self):
        return self._city_plans_won

    @city_plans_won.setter
    def city_plans_won(self, city_plans_won: list) -> None:
        if not check_valid_lst(city_plans_won, 3, lambda x: type(x) == bool):
            raise GameStateException(f"Given {city_plans_won}, but city_plans_won must be a list of length 3 containing booleans.")
        self._city_plans_won = city_plans_won

    @property 
    def ccards(self):
        return self._ccards

    @ccards.setter
    def ccards(self, ccards) -> None:
        if not check_valid_lst(ccards, 3, lambda x: type(x) == list):
            raise GameStateException(f"Given {ccards}, but construction cards must be a list of 3 lists.")
        self._ccards = [ConstructionCard(cc) for cc in ccards]

    @property
    def effects(self):
        return self._effects

    @effects.setter
    def effects(self, effects: list) -> None:
        if not check_valid_lst(effects, 3, lambda x: type(x) == str):
            raise GameStateException(f"Given {effects}, but effects must be a list of string of length 3.")
        self._effects = [Effect(e) for e in effects]

    def to_dict(self) -> dict:
        '''
        Returns the Dictionary representation of a GameState.
        '''
        dict_repr = {
            "city-plans": [cp.to_dict() for cp in self._city_plans],
            "city-plans-won": self._city_plans_won,
            "construction-cards": [cc.to_list() for cc in self._ccards],
            "effects": [str(effect) for effect in self._effects]
        }
        return dict_repr

    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a GameState.
        '''
        return json.dumps(self.to_dict())

    def __eq__(self, other: object) -> bool:
        return self.to_dict() == other.to_dict()
