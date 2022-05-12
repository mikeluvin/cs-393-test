import unittest
from player_state import *
from exception import *

class TestHome(unittest.TestCase):
    # blank house state
    def test_valid_blank(self):
        home_lst = [False, "blank", False, False]
        home = Home(home_lst)
        self.assertEqual(home.to_list(), home_lst[:3])

    # try to use a blank in housing plan
    def test_invalid_blank_ip(self):
        home_lst = [False, "blank", True, False]
        with self.assertRaises(HomeException):
            Home(home_lst)

    # pass a non-list into constructor
    def test_invalid_constructor_arg(self):
        home_lst = "hi"
        with self.assertRaises(HomeException):
            Home(home_lst)

    # pass a list with the wrong order of types
    def test_invalid_constructor_list(self):
        home_lst = ["blank", False, True, False]
        with self.assertRaises(HomeException):
            Home(home_lst)
    
    # pass a valid bis house
    def test_valid_bis(self):
        home_lst = [False, [6, "bis"], False, False]
        home = Home(home_lst)
        self.assertEqual(home.to_list(), home_lst[:3])
    
    # pass a valid house number
    def test_valid_house(self):
        home_lst = [False, 5, False, False]
        home = Home(home_lst)
        self.assertEqual(home.to_list(), home_lst[:3])

    # pass a valid house number in plan
    def test_valid_house_ip(self):
        home_lst = [False, 17, True, False]
        home = Home(home_lst)
        self.assertEqual(home.to_list(), home_lst[:3])

    # pass a house number greater than 17 
    def test_invalid_house_number1(self):
        home_lst = [False, 18, False, False]
        with self.assertRaises(HomeException):
            Home(home_lst)
        
    # pass a house with number -1
    def test_invalid_house_number2(self):
        home_lst = [False, -1, False, False]
        with self.assertRaises(HomeException):
            Home(home_lst)

    # pass a floating point house number
    def test_invalid_house_number3(self):
        home_lst = [False, 0.11, True, False]
        with self.assertRaises(HomeException):
            Home(home_lst)

    # pass a non-integer house number
    def test_invalid_house_number4(self):
        home_lst = [False, "house1", True, False]
        with self.assertRaises(HomeException):
            Home(home_lst)

    # pass a valid roundabout house
    def test_valid_roundabout(self):
        home_lst = [True, "roundabout", False, True]
        home = Home(home_lst)
        self.assertEqual(home.to_list(), home_lst[:3])
    
    # pass a invalid roundabout house, no left fence
    def test_invalid_roundabout1(self):
        home_lst = [False, "roundabout", False, True]
        with self.assertRaises(HomeException):
            Home(home_lst)
        
    # pass a invalid roundabout house, no fences
    def test_invalid_roundabout2(self):
        home_lst = [False, "roundabout", False, False]
        with self.assertRaises(HomeException):
            Home(home_lst)
    
    # pass a invalid roundabout house, marked used-in-plan
    def test_invalid_roundabout3(self):
        home_lst = [True, "roundabout", True, True]
        with self.assertRaises(HomeException):
            Home(home_lst)
    
class TestStreet(unittest.TestCase):
    # additional keys
    def test_addtl_keys(self):
        st_dict = {
            "homes": [],
            "parks": 0,
            "pools": [],
            "pandas": 6
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # incorrect keys
    def test_incorrect_keys(self):
        st_dict = {
            "homie": [],
            "parks": 0,
            "pools": [],
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # missing keys
    def test_missing_keys(self):
        st_dict = {
            "homes": [],
            "pools": [],
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # pass in a non-dictionary type
    def test_nondict_type(self):
        st_dict = ["homes", "parks", "pools"]
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # incorrect value types
    def test_incorrect_types(self):
        st_dict = {
            "homes": ["a", "b", "c"],
            "parks": 0,
            "pools": [False, False, False],
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    def test_valid_street(self):
        st_dict = {
            "homes": [1,False,[True,2,True],[False,3,True],[False,4,True],[True,5,False],[False,6,False],[False,7,False],[False,8,False],[False,9,False],[False,10,False]],
            "parks": 3,
            "pools": [False,True,True]
        }
        street = Street(st_dict, 0)
        self.assertEqual(street.to_dict(), st_dict)
        
    # validate homes: strictly increasing (except for bis)  
    # bis must be the same number as an adjacent house 
    def test_valid_street_bis(self):
        st_dict = {
            "homes": [1,False,[True,2,True],[False,[2, "bis"],True],[False,4,True],[True,5,False],[False,6,False],[False,7,False],[False,"blank",False],[False,9,False],[False,10,False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        # test first street, then second, then third
        street = Street(st_dict, 0)
        self.assertEqual(street.to_dict(), st_dict)

        st_dict["homes"].append([False, 11, False])
        street1 = Street(st_dict, 1)
        self.assertEqual(street1.to_dict(), st_dict)

    # at least one bis must be next to a non-bis house
    def test_invalid_street_bis_start(self):
        st_dict = {
            "homes": [[2, "bis"],False,[False,[2, "bis"],True],[False,[2, "bis"],True],[False,"blank",False],[True,5,False],[False,6,False],[False,7,False],[False,"blank",False],[False,9,False],[False,10,False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    def test_invalid_street_bis_middle_occupied(self):
        st_dict = {
            "homes": [1,False,[False,[2, "bis"],True],[False,[2, "bis"],True],[False,[2, "bis"],False],[True,5,False],[False,6,False],[False,7,False],[False,"blank",False],[False,9,False],[False,10,False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # at least one bis must be next to a non-bis house
    def test_invalid_street_bis_middle_rest_blank(self):
        st_dict = {
            "homes": ["blank",False,[False,[2, "bis"],True],[False,[2, "bis"],True],[False,"blank",False],[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # at least one bis must be next to a non-bis house
    def test_invalid_street_bis_two_separated_bis_blocks(self):
        st_dict = {
            "homes": ["blank",False,[False,[2, "bis"],True],[False,[2, "bis"],True],[False,[2, "bis"],False],[True,"blank",False],[False,"blank",False],[False,[2, "bis"],True],[False,[2, "bis"],True],[False,[2, "bis"],False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)


    # at least one bis must be next to a non-bis house
    def test_invalid_street_bis_two_adjacent_bis_blocks(self):
        st_dict = {
            "homes": ["blank",False,[False,[2, "bis"],True],[False,[2, "bis"],True],[False,[4, "bis"],False],[False,[4, "bis"],True],[False,[4, "bis"],True],[False,[4, "bis"],False],[True,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    def test_valid_street_bis_two_adjacent_bis_blocks(self):
        st_dict = {
            "homes": [2,False,[False,[2, "bis"],True],[False,[2, "bis"],True],[False,[4, "bis"],False],[False,[4, "bis"],True],[False,[4, "bis"],True],[False,4,False],[True,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        street = Street(st_dict, 0)
        self.assertEqual(street.to_dict(), st_dict)

    # at least one bis must be next to a non-bis house
    def test_invalid_street_bis_end_rest_blank(self):
        st_dict = {
            "homes": ["blank",False,[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,[2, "bis"],True],[False,[2, "bis"],True],[False,[2, "bis"],False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # at least one bis must be next to a non-bis house
    def test_invalid_street_bis_all_bis(self):
        st_dict = {
            "homes": [[2, "bis"],False,[True,[2, "bis"],False],[False,[2, "bis"],False],[False,[2, "bis"],False],[False,[2, "bis"],False],[False,[2, "bis"],False],[False,[2, "bis"],False],[False,[2, "bis"],True],[False,[2, "bis"],True],[False,[2, "bis"],False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)
    
    def test_street_incorrect_order(self):
        st_dict = {
            "homes": [1,False,[True,2,True],[False,2,True],[False,4,True],[True,5,False],[False,6,False],[False,7,False],[False,8,False],[False,9,False],[False,10,False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)
        
    # bis cannot have a pool  
    def test_invalid_bis_pool(self):
        st_dict = {
            "homes": ["blank",False,[False,2,False],[False,[2, "bis"],False],[False,"blank",False],[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [True, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)
              
    # bis can't be separated from its duplicate by a fence 
    def test_invalid_bis_fence(self):
        st_dict = {
            "homes": [1,False,[True,[2, "bis"],True],[True,2,True],[False,4,True],[True,5,False],[False,6,False],[False,7,False],[False,8,False],[False,9,False],[False,10,False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # can bis a bis
    def test_valid_bis_bis(self):
        st_dict = {
            "homes": [1,False,[True,2,True],[False,[2, "bis"],True],[False,[2, "bis"],True],[True,5,False],[False,6,False],[False,7,False],[False,8,False],[False,9,False],[False,10,False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        street = Street(st_dict, 0)
        self.assertEqual(street.to_dict(), st_dict)
    
     
    # number of parks is <= number of non-bis houses on this street
    def test_invalid_parks(self):
        st_dict = {
            "homes": ["blank",False,[False,2,False],[False,[2, "bis"],False],[False,"blank",False],[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 3,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # bis next to blank house
    def test_invalid_bis_no_adjacent_house(self):
        st_dict = {
            "homes": ["blank",False,[False,"blank",False],[False,[2, "bis"],False],[False,"blank",False],[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)
    
    # bis house number and adjacent house number different
    def test_invalid_bis_incorrect_house_number(self):
        st_dict = {
            "homes": ["blank",False,[False,1,False],[False,[2, "bis"],False],[False,"blank",False],[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)
    
    # number of pools <= # houses in row  
    def test_invalid_total_pool(self):
        st_dict = {
            "homes": ["blank",False,[False,"blank",False],[False,2,False],[False,"blank",False],[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [True, True, True]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)
    
    # two correct adjacent bis houses   
    def test_adjacent_bis_houses(self):
        st_dict = {
            "homes": ["blank",False,[False,2,False],[False,[2, "bis"],False],[False,[3, "bis"],False],[False,3,False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        street = Street(st_dict, 0)
        self.assertEqual(street.to_dict(), st_dict)

    # sandwich bis case
    def test_sandwich_bis_houses(self):
        st_dict = {
            "homes": ["blank",False,[False,"blank",False],[False,[2, "bis"],False],[False,2,False],[False,[2, "bis"],False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        street = Street(st_dict, 0)
        self.assertEqual(street.to_dict(), st_dict)

    # incorrect row number
    def test_incorrect_row_number(self):
        st_dict = {
            "homes": ["blank",False,[False,"blank",False],[False,[2, "bis"],False],[False,2,False],[False,[2, "bis"],False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # valid roundabout
    def test_valid_roundabout(self):
        st_dict = {
            "homes": ["blank",False,[False,2,False],[False,[2, "bis"],False],[True,"roundabout",False],[True,1,False],[False,"blank",False],[False,5,False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        street = Street(st_dict, 0)
        self.assertEqual(street.to_dict(), st_dict)

    # bis on opposite side of roundabout
    def test_invalid_bis_roundabout(self):
        st_dict = {
            "homes": ["blank",False,[False,1,False],[False,[2, "bis"],False],[True,"roundabout",False],[True,2,False],[False,"blank",False],[False,5,False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # 3 parks but only two non-bis houses
    def test_invalid_parks_roundabout(self):
        st_dict = {
            "homes": ["blank",False,[False,2,False],[False,[2, "bis"],False],[True,"roundabout",False],[True,1,False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 3,
            "pools": [False, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

    # roundabout cannot have a pool  
    def test_invalid_roundabout_pool(self):
        st_dict = {
            "homes": ["blank",False,[False,"blank",False],[True,"roundabout",False],[True,"blank",False],[True,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False],[False,"blank",False]],
            "parks": 0,
            "pools": [True, False, False]
        }
        with self.assertRaises(StreetException):
            Street(st_dict, 0)

if __name__ == "__main__":
    unittest.main()