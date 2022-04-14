import json

EFFECTS = set(["surveyor", "agent", "landscaper", "pool", "temp", "bis"])


def check_nat(num: int):
    '''
    Returns True if the input is a natural number.
    '''
    return type(num) == int and num >= 0


def check_valid_lst(lst: list, length: int, valid_func):
    '''
    Returns True if all elements in the list satisfy the constraints in 
    valid_func and the list is the desired length.
    '''
    if type(lst) != list or (length is not None and len(lst) != length):
        return False

    return all(valid_func(x) for x in lst)


def check_type_and_membership(var, typ, set_):
    '''
    Returns True if var is of type typ and is in set_.
    '''
    return type(var) == typ and var in set_


def check_increasing(lst):
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            return False

    return True


class CityPlan():
    def __init__(self, cp_dict) -> None:
        cp_keys = set(["criteria", "position", "score1", "score2"])
        if type(cp_dict) != dict or set(cp_dict.keys()) != cp_keys:
            raise ValueError(f"A city-plan must be a dictionary containing only these keys: {cp_keys}")
        criteria, position, score1, score2 = cp_dict["criteria"], cp_dict["position"], cp_dict["score1"], cp_dict["score2"]

        # valid city plan positions are 1, 2, or 3
        valid_posns = set(range(1, 4))
        # criteria must be a list of naturals
        if not check_valid_lst(criteria, None, check_nat) or not check_increasing(criteria):
            raise ValueError(f"Given {criteria}, but city plan 'criteria' must be a list of integers.")
        self._criteria = criteria
       
        if not check_type_and_membership(position, int, valid_posns):
            raise ValueError(f"Given {position}, but city plan 'position' must be either 1, 2, or 3.")
        self._position = position

        # scores must be naturals
        if not check_nat(score1):
            raise ValueError(f"Given {score1}, but city plan 'score1' must be a natural.")
        self._score1 = score1

        if not check_nat(score2):
            raise ValueError(f"Given {score2}, but city plan 'score1' must be a natural.")
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


class ConstructionCard():
    def __init__ (self, cc_lst) -> None:
        if type(cc_lst) != list or len(cc_lst) != 2:
            raise ValueError(f"The input for construction-card must be [ int, string ]")

        num, effect = cc_lst
        # valid range of card number is 1-15
        valid_range = set(range(1, 16))

        # validate class inputs based on game spec
        if not check_type_and_membership(num, int, valid_range):
            raise ValueError(f"Given {num}, but card numbers must be an integer between 1 and 15.")
        self._num = num

        if not check_type_and_membership(effect, str, EFFECTS):
            raise ValueError(f"Given {effect}, but effect must be one of {EFFECTS}.")
        self._effect = effect

    def to_list(self) -> list:
        '''
        Returns the list representation of ConstructionCard, as outlined in the Assignment 3 spec.
        '''
        return [self._num, self._effect]

    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a ConstructionCard.
        '''
        return json.dumps(self.to_list())



class GameState():
    def __init__(self, gs_dict) -> None:
        gs_keys = set(["city-plans", "city-plans-won", "construction-cards", "effects"])
        if type(gs_dict) != dict or set(gs_dict.keys()) != gs_keys:
            raise ValueError(f"A game-state must be a dictionary containing only these keys: {gs_keys}")

        city_plans, city_plans_won = gs_dict["city-plans"], gs_dict["city-plans-won"]
        construct_cards, effects = gs_dict["construction-cards"], gs_dict["effects"]

        if not check_valid_lst(city_plans, 3, lambda x: type(x) == dict):
            raise ValueError(f"Given {city_plans}, but city_plans must be a list of 3 dictionaries.")
        
        cp_posns = set([cp.get("position", -1) for cp in city_plans])
        if cp_posns != set([1, 2, 3]):
            raise ValueError(f"The list of city-plans must have three plans with unique positions 1, 2, and 3.")
        self._city_plans = [CityPlan(cp) for cp in city_plans]

        if not check_valid_lst(city_plans_won, 3, lambda x: type(x) == bool):
            raise ValueError(f"Given {city_plans_won}, but city_plans_won must be a list of length 3 containing booleans.")
        self._city_plans_won = city_plans_won

        if not check_valid_lst(construct_cards, 3, lambda x: type(x) == list):
            raise ValueError(f"Given {city_plans}, but city_plans must be a list of 3 lists.")
        self._construct_cards = [ConstructionCard(cc) for cc in construct_cards]

        if not check_valid_lst(effects, 3, lambda x: check_type_and_membership(x, str, EFFECTS)):
            raise ValueError(f"Given {effects}, but effects must be a list of length 3 containing one of {EFFECTS}.")
        self._effects = effects

    # the city_plans_won, construction_cards, and effects fields are all updated as the game progresses
    # while not necessary for this assignment, in the future we may use the 'property' decorator
    # (see https://docs.python.org/3/library/functions.html#property)
    # to make for an easier getter/setter API and to enforce the field constraints.
    '''
    @property
    def city_plans(self):
        """The 'city_plans' field, a list of length 3 containing CityPlan objects."""
        return self._city_plans

    @num.setter
    def city_plans(self, new_city_plans):
        if not check_valid_lst(new_city_plans, 3, lambda x: isinstance(x) == CityPlan):
            raise ValueError(f"Given {new_city_plans}, but city_plans must be a list of length 3 containing CityPlan objects.")
        
        self._city_plans = new_city_plans
    '''

    def to_dict(self) -> dict:
        '''
        Returns the Dictionary representation of a GameState.
        '''
        dict_repr = {
            "city-plans": [cp.to_dict() for cp in self._city_plans],
            "city-plans-won": self._city_plans_won,
            "construction-cards": [cc.to_list() for cc in self._construct_cards],
            "effects": self._effects
        }
        return dict_repr

    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a GameState.
        '''
        return json.dumps(self.to_dict())
