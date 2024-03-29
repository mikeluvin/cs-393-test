import unittest
from game_state import *
from exception import *

class TestCityPlan(unittest.TestCase):
    def test_valid_cp(self):
        cp_dict = {
            "criteria": [1,1,2,6],
            "position": 1,
            "score1": 8,
            "score2": 4
        }
        cp = CityPlan(cp_dict)
        self.assertEqual(cp.to_dict(), cp_dict)

    def test_cp_not_increasing_order(self):
        cp_dict = {
            "criteria": [8,4,2,6],
            "position": 1,
            "score1": 8,
            "score2": 4
        }
        with self.assertRaises(CityPlanException):
            CityPlan(cp_dict)

    def test_valid_special_criteria1(self):
        criteria_1 = [
            [ "all houses", 0 ],
            [ "all houses", 2 ],
            "end houses",
            "7 temps",
            "5 bis"
        ]
        cp_dict = {
            "position": 1,
            "score1": 8,
            "score2": 4
        }
        for criteria in criteria_1:
            cp_dict["criteria"] = criteria
            cp = CityPlan(cp_dict)
            self.assertEqual(cp.to_dict(), cp_dict)

    def test_invalid_special_criteria1(self):
        bad_criteria = [
            [ "all houses", 1 ],
            [ "all houses", 3 ],
            "end house",
            "2 temps",
            "9 bis",
            # criteria 2 cards
            "two streets all parks",
            "two streets all pools",
            [ "all pools all parks", 1 ],
            [ "all pools all parks", 2 ],
            "all pools all parks one roundabout"
        ]
        cp_dict = {
            "position": 1,
            "score1": 8,
            "score2": 4
        }
        for criteria in bad_criteria:
            cp_dict["criteria"] = criteria
            with self.assertRaises(CityPlanException):
                CityPlan(cp_dict)

    def test_valid_special_criteria2(self):
        criteria_2 = [
            "two streets all parks",
            "two streets all pools",
            [ "all pools all parks", 1 ],
            [ "all pools all parks", 2 ],
            "all pools all parks one roundabout"
        ]
        cp_dict = {
            "position": 2,
            "score1": 8,
            "score2": 4
        }
        for criteria in criteria_2:
            cp_dict["criteria"] = criteria
            cp = CityPlan(cp_dict)
            self.assertEqual(cp.to_dict(), cp_dict)

    def test_invalid_special_criteria2(self):
        bad_criteria = [
            "two streets no parks",
            "two streets two pools",
            [ "all pools all parks", 0 ],
            [ "all pools no parks", 2 ],
            "all pools one park one roundabout",
            # criteria1 cards
            [ "all houses", 0 ],
            [ "all houses", 2 ],
            "end houses",
            "7 temps",
            "5 bis"
        ]
        cp_dict = {
            "position": 2,
            "score1": 8,
            "score2": 4
        }
        for criteria in bad_criteria:
            cp_dict["criteria"] = criteria
            with self.assertRaises(CityPlanException):
                CityPlan(cp_dict)
    
    def test_invalid_special_criteria_in_posn3(self):
        bad_criteria = [
            # criteria1 cards
            [ "all houses", 0 ],
            [ "all houses", 2 ],
            "end houses",
            "7 temps",
            "5 bis"
            # criteria 2 cards
            "two streets all parks",
            "two streets all pools",
            [ "all pools all parks", 1 ],
            [ "all pools all parks", 2 ],
            "all pools all parks one roundabout"
        ]
        cp_dict = {
            "position": 3,
            "score1": 8,
            "score2": 4
        }
        for criteria in bad_criteria:
            cp_dict["criteria"] = criteria
            with self.assertRaises(CityPlanException):
                CityPlan(cp_dict)

class TestEffects(unittest.TestCase):
    def test_valid_effects(self):
        effects_lst = ["agent", "surveyor", "temp", "pool", "agent", "bis", "landscaper"]
        for effect_str in effects_lst:
            effect = Effect(effect_str)
            self.assertEqual(str(effect), effect_str)

    def test_invalid_effects(self):
        effects_str = "poool"
        with self.assertRaises(EffectException):
            Effect(effects_str)

class TestConstructionCards(unittest.TestCase):
    def test_valid_ccards(self):
        ccards_lst = [1,"surveyor"]
        ccards = ConstructionCard(ccards_lst)
        self.assertEqual(ccards.to_list(), ccards_lst)
    
    def test_invalid_ccards_number(self):
        ccards_lst = [16, "pool"]
        with self.assertRaises(ConstructionCardException):
            ConstructionCard(ccards_lst)

    def test_invalid_ccards_effect(self):
        ccards_lst = [16, "pools"]
        with self.assertRaises(ConstructionCardException):
            ConstructionCard(ccards_lst)


if __name__ == "__main__":
    unittest.main()