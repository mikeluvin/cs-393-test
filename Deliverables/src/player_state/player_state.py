import json
from typing import *
from helpers import *
from exception import PlayerStateException, my_assert
from . import Street
from collections import defaultdict
from constants import EMPTY_PS, MAX_REFUSALS, AGENT_MAXES, MAX_TEMPS, TEMP_SCORES

class PlayerState():
    def __init__(self, ps_dict: Dict=EMPTY_PS) -> None:
        ps_keys = set(["agents", "city-plan-score", "refusals", "streets", "temps"])
        my_assert(type(ps_dict) == dict and set(ps_dict.keys()) == ps_keys,
            PlayerStateException,
            f"A player-state must be a dictionary containing only these keys: {ps_keys}")

        agents, cp_scores, refusals = ps_dict["agents"], ps_dict["city-plan-score"], ps_dict["refusals"]
        streets, temps = ps_dict["streets"], ps_dict["temps"]

        self.agents = agents
        self.city_plan_score = cp_scores
        self.refusals = refusals
        self.streets = streets
        self.temps = temps

    def _validate_agents(self, agents: List[int]) -> bool:
        '''
        Returns True if the following are True:
        1. agents is a list of 6 naturals
        2. each element is within its respective maximum value.
        '''
        return check_valid_lst(agents, 6, check_nat) and all(a <= AGENT_MAXES[i] for i, a in enumerate(agents))

    @property
    def streets(self) -> List[Street]:
        '''
        Returns the list of Street objects for this PlayerState.
        '''
        return self._streets

    @streets.setter
    def streets(self, streets: List) -> None:
        my_assert(check_valid_lst(streets, 3, lambda x: type(x) == dict),
            PlayerStateException,
            f"Given {streets}, but streets must be a list 3 dictionaries.")
        self._streets = [Street(st, i) for i, st in enumerate(streets)]

        num_roundabouts = sum([street.roundabout_count() for street in self._streets])
        my_assert(num_roundabouts <= 2,
            PlayerStateException,
            f"You can only play two roundabouts in a game.")

    @property
    def agents(self) -> List[int]:
        '''
        Returns the list of agents for this PlayerState.
        '''
        return self._agents

    @agents.setter
    def agents(self, agents: List[int]) -> None:
        my_assert(self._validate_agents(agents),
            PlayerStateException,
            f"Given {agents}, but agents must be a list of 6 naturals.")
        self._agents = agents

    @property
    def city_plan_score(self) -> List[Union[int, str]]:
        return self._cp_scores

    @city_plan_score.setter
    def city_plan_score(self, cp_scores: list):
        my_assert(check_valid_lst(cp_scores, 3, lambda x: (check_nat(x) or x == "blank")),
            PlayerStateException,
            f"Given {cp_scores}, but city_plan_scores must be a list containing naturals or 'blank'.")
        self._cp_scores = cp_scores
    
    @property
    def refusals(self) -> int:
        return self._refusals

    @refusals.setter
    def refusals(self, refusals: int) -> None:
        my_assert(check_nat(refusals) and refusals <= MAX_REFUSALS,
            PlayerStateException,
            f"Given {refusals}, but refusals must be either 0, 1, 2, or 3.")
        self._refusals = refusals

    @property
    def temps(self) -> int:
        return self._temps

    @temps.setter
    def temps(self, temps: int) -> None:
        my_assert(check_nat(temps) and temps <= MAX_TEMPS,
            PlayerStateException,
            f"Given {temps}, but temps must be an integer between 0 and 11.")
        self._temps = temps
    
    @property
    def roundabouts(self) -> int:
        return sum([street.roundabout_count() for street in self._streets])

    def temps_score(self, temps_lst: List[int]) -> int:
        if self._temps == 0:
            return 0

        if not temps_lst:
            return TEMP_SCORES[0]

        temps_lst.append(self._temps)
        sorted_temps_lst = list(set(temps_lst))
        sorted_temps_lst.sort(reverse=True)
        rank = sorted_temps_lst.index(self._temps)
        return TEMP_SCORES[rank] if rank < 3 else 0

    def total_cp_scores(self) -> int:
        total = 0
        for score in self._cp_scores:
            if score != "blank":
                total += score
        
        return total

    def calculate_score(self, temps_lst: List[int]) -> int:
        total_score = 0
        pools_count = 0
        bis_count = 0
        estates_count_dict = defaultdict(int)
        estate_scores = {
            1: [1, 3], 
            2: [2, 3, 4],
            3: [3, 4, 5, 6],
            4: [4, 5, 6, 7, 8],
            5: [5, 6, 7, 8, 10],
            6: [6, 7, 8, 10, 12] 
        }
        pools_score = [0, 3, 6, 9, 13, 17, 21, 26, 31, 36]
        bis_score = [0, 1, 3, 6, 9, 12, 16, 20, 24, 28]
        refusal_score = [0, 0, 3, 5]
        roundabout_score = [0, 3, 8]
        for street in self._streets:
            pools_count += street.pools_built()
            bis_count += street.bis_count()
            # total estates count
            for size, ct in street.estates_dict().items():
                estates_count_dict[size] += ct

            total_score += street.parks_score()
        
        estates_total_score = 0
        for size, ct in estates_count_dict.items():
            agent_ct = self._agents[size - 1]
            estates_total_score += estate_scores[size][agent_ct] * ct

        total_score += pools_score[pools_count]
        total_score += self.total_cp_scores()
        total_score += self.temps_score(temps_lst)
        total_score += estates_total_score
        total_score -= bis_score[bis_count]
        total_score -= refusal_score[self._refusals]
        total_score -= roundabout_score[self.roundabouts]

        return total_score

    def is_game_over(self) -> bool:
        return (self.refusals == MAX_REFUSALS or 
            all([s.is_full() for s in self._streets]) or 
            all([score != "blank" for score in self._cp_scores]))

        
    def to_dict(self) -> Dict:
        '''
        Returns the Dictionary representation of a PlayerState.
        '''
        dict_repr = {
            "agents": self._agents,
            "city-plan-score": self._cp_scores,
            "refusals": self._refusals,
            "streets": [street.to_dict() for street in self._streets],
            "temps": self._temps
        }

        return dict_repr
    
    def __repr__(self) -> str:
        '''
        Returns the JSON representation of a PlayerState.
        '''
        return json.dumps(self.to_dict())

    def __eq__(self, other: object) -> bool:
        return type(other) == PlayerState and self.to_dict() == other.to_dict()

