import json
from player_state import PlayerState, Street
from exception import CriteriaException, MoveException
from helpers import * 
from constants import PARK_MAXES, VALID_CRITERIA_CARDS, CriteriaCard

class Criteria():
    def __init__(self, criteria, position) -> None:
        # criteria must be a list of naturals, or one of the special cases (below)
        self._is_incr_lst_ints = check_valid_lst(criteria, None, check_nat) and check_increasing(criteria)
        if not self._is_incr_lst_ints:
            # then check if it's one of the special cases
            try:
                criteria = CriteriaCard(criteria)
            except ValueError:
                raise CriteriaException(f"Given '{criteria}', but city plan 'criteria' must be a list of \
                    integers or one of the specified criteria cards.")
            if not (position < 3 and criteria in VALID_CRITERIA_CARDS[position-1]):
                raise CriteriaException(f"Given '{criteria}', but city plan 'criteria' must be a list of \
                    integers or one of the specified criteria cards.")
        self._valid_criteria = criteria

    def is_satisfied(self, player_state: PlayerState, estates) -> bool:
        if self._is_incr_lst_ints:
            return self._is_num_criteria_satisfied(estates)
        elif self._valid_criteria == CriteriaCard.ALL_HOUSES_0:
            return self._is_all_houses_satisfied(player_state.streets[0])
        elif self._valid_criteria == CriteriaCard.ALL_HOUSES_2:
            return self._is_all_houses_satisfied(player_state.streets[2])
        elif self._valid_criteria == CriteriaCard.END_HOUSES:
            return self._is_end_houses_satisfied(player_state.streets)
        elif self._valid_criteria == CriteriaCard.SEVEN_TEMPS:
            return self._is_7_temps_satisfied(player_state.temps)
        elif self._valid_criteria == CriteriaCard.FIVE_BIS:
            return self._is_5_bis_satisfied(player_state.streets)
        elif self._valid_criteria == CriteriaCard.TWO_STREETS_ALL_PARKS:
            return self._is_two_streets_all_parks_satisfied(player_state.streets)
        elif self._valid_criteria == CriteriaCard.TWO_STREETS_ALL_POOLS:
            return self._is_two_streets_all_pools_satisfied(player_state.streets)
        elif self._valid_criteria == CriteriaCard.ALL_POOLS_ALL_PARKS_1:
            return self._is_all_pools_all_parks_satisfied(player_state.streets[1], 1)
        elif self._valid_criteria == CriteriaCard.ALL_POOLS_ALL_PARKS_2:
            return self._is_all_pools_all_parks_satisfied(player_state.streets[2], 2)
        elif self._valid_criteria == CriteriaCard.ALL_POOLS_ALL_PARKS_ONE_ROUNDABOUT:
            return self._is_all_pools_all_parks_one_roundabout_satisfied(player_state.streets)

        raise CriteriaException(f"should never get here lol")

    def _is_num_criteria_satisfied(self, estates) -> bool:
        # loop through estate size values in criteria and see
        # if there's estates matching those sizes
        for estate_size in self._valid_criteria:
            if estate_size in estates:
                estates[estate_size] -= 1
                if estates[estate_size] == 0:
                    del estates[estate_size]
            else:
                # then, the player tried claiming the points for 
                # this city plan, but they don't have the correct estates
                return False
        return True

    def _is_all_houses_satisfied(self, street: Street) -> bool:
        return all([type(h.num) == int and h.in_plan for h in street.homes])

    def _is_end_houses_satisfied(self, streets) -> bool:
        for street in streets:
            first_home, last_home = street.homes[0], street.homes[-1]
            if not (type(first_home.num) == int and first_home.in_plan 
                and type(last_home.num) == int and last_home.in_plan):
                return False

        return True

    def _is_7_temps_satisfied(self, temps) -> bool:
        return temps >= 7

    def _is_5_bis_satisfied(self, streets) -> bool:
        return any([s.bis_count() >= 5 for s in streets])

    def _is_two_streets_all_parks_satisfied(self, streets):
        return [s.parks == PARK_MAXES[i] for i, s in enumerate(streets)].count(True) >= 2

    def _is_two_streets_all_pools_satisfied(self, streets):
        return [all(s.pools) for s in streets].count(True) >= 2

    def _is_all_pools_all_parks_satisfied(self, street: Street, st_idx: int):
        return all(street.pools) and street.parks == PARK_MAXES[st_idx]

    def _is_all_pools_all_parks_one_roundabout_satisfied(self, streets):
        return any([self._is_all_pools_all_parks_satisfied(s, i) and s.roundabout_count() > 0 for i, s in enumerate(streets)])

    def to_list_or_string(self):
        return self._valid_criteria if self._is_incr_lst_ints else self._valid_criteria.value

    def __repr__(self) -> str:
        return json.dumps(self.to_list_or_string())
