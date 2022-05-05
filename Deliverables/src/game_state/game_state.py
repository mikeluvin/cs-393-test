import json
from exception import *
from helpers import *
from . import CityPlan, Effect, ConstructionCard

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
