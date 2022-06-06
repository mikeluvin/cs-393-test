import json
from typing import *
from exception import GameStateException, my_assert
from helpers import *
from . import CityPlan, Effect, ConstructionCard

class GameState():
    def __init__(self, gs_dict: Dict) -> None:
        gs_keys = set(["city-plans", "city-plans-won", "construction-cards", "effects"])
        my_assert(type(gs_dict) == dict and set(gs_dict.keys()) == gs_keys,
            GameStateException,
            f"A game-state must be a dictionary containing only these keys: {gs_keys}")

        city_plans, city_plans_won = gs_dict["city-plans"], gs_dict["city-plans-won"]
        construct_cards, effects = gs_dict["construction-cards"], gs_dict["effects"]

        self.city_plans = city_plans
        self.city_plans_won = city_plans_won
        self.ccards = construct_cards
        self.effects = effects
    
    @property
    def city_plans(self) -> List[CityPlan]:
        """The 'city_plans' field, a list of length 3 containing CityPlan objects."""
        return self._city_plans

    @city_plans.setter
    def city_plans(self, city_plans: List[Dict]):
        my_assert(check_valid_lst(city_plans, 3, lambda x: type(x) == dict),
            GameStateException,
            f"Given {city_plans}, but city_plans must be a list of 3 dictionaries.")

        cp_posns = set([cp.get("position", -1) for cp in city_plans])
        my_assert(cp_posns == set([1, 2, 3]),
            GameStateException,
            f"The list of city-plans must have three plans with unique positions 1, 2, and 3.")
        self._city_plans = [CityPlan(cp) for cp in city_plans]
    
    @property
    def city_plans_won(self) -> List[bool]:
        return self._city_plans_won

    @city_plans_won.setter
    def city_plans_won(self, city_plans_won: List[bool]) -> None:
        my_assert(check_valid_lst(city_plans_won, 3, lambda x: type(x) == bool),
            GameStateException,
            f"Given {city_plans_won}, but city_plans_won must be a list of length 3 containing booleans.")
        self._city_plans_won = city_plans_won

    @property 
    def ccards(self) -> List[ConstructionCard]:
        return self._ccards

    @ccards.setter
    def ccards(self, ccards: List[List]) -> None:
        my_assert(check_valid_lst(ccards, 3, lambda x: type(x) == list),
            GameStateException,
            f"Given {ccards}, but construction cards must be a list of 3 lists.")
        self._ccards = [ConstructionCard(cc) for cc in ccards]

    @property
    def effects(self) -> List[Effect]:
        return self._effects

    @effects.setter
    def effects(self, effects: List[str]) -> None:
        my_assert(check_valid_lst(effects, 3, lambda x: type(x) == str),
            GameStateException,
            f"Given {effects}, but effects must be a list of string of length 3.")
        self._effects = [Effect(e) for e in effects]

    def to_dict(self) -> Dict:
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
        return type(other) == GameState and self.to_dict() == other.to_dict()
