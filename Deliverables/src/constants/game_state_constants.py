from enum import Enum
import json

NUM_CCS = 3
NUM_CPS = 3
# valid city plan positions are 1, 2, or 3
VALID_POSNS = set(range(1, 4))

class CriteriaCard(Enum):
    ALL_HOUSES_0 = [ "all houses", 0 ]
    ALL_HOUSES_2 = [ "all houses", 2 ]
    END_HOUSES = "end houses"
    SEVEN_TEMPS = "7 temps"
    FIVE_BIS = "5 bis"
    TWO_STREETS_ALL_PARKS = "two streets all parks"
    TWO_STREETS_ALL_POOLS = "two streets all pools"
    ALL_POOLS_ALL_PARKS_1 = [ "all pools all parks", 1 ]
    ALL_POOLS_ALL_PARKS_2 = [ "all pools all parks", 2 ]
    ALL_POOLS_ALL_PARKS_ONE_ROUNDABOUT = "all pools all parks one roundabout"

    def __repr__(self) -> str:
        return json.dumps(self.value)


VALID_CRITERIA_CARDS = [
    [
        CriteriaCard.ALL_HOUSES_0,
        CriteriaCard.ALL_HOUSES_2,
        CriteriaCard.END_HOUSES,
        CriteriaCard.SEVEN_TEMPS,
        CriteriaCard.FIVE_BIS
    ],
    [
        CriteriaCard.TWO_STREETS_ALL_PARKS,
        CriteriaCard.TWO_STREETS_ALL_POOLS,
        CriteriaCard.ALL_POOLS_ALL_PARKS_1,
        CriteriaCard.ALL_POOLS_ALL_PARKS_2,
        CriteriaCard.ALL_POOLS_ALL_PARKS_ONE_ROUNDABOUT
    ]
]

CITY_PLAN_CARDS = [
    {"criteria":[1,1,1,1,1,1],"position":1,"score1":8,"score2":4},
    {"criteria":[2,2,2,2],"position":1,"score1":8,"score2":4},
    {"criteria":[3,3,3],"position":1,"score1":8,"score2":4},
    {"criteria":[4,4],"position":1,"score1":6,"score2":3},
    {"criteria":[5,5],"position":1,"score1":8,"score2":4},
    {"criteria":[6,6],"position":1,"score1":10,"score2":6},
    {"criteria":["all houses",0],"position":1,"score1":6,"score2":3},
    {"criteria":["all houses",2],"position":1,"score1":8,"score2":4},
    {"criteria":"end houses","position":1,"score1":7,"score2":4},
    {"criteria":"5 bis","position":1,"score1":8,"score2":3},
    {"criteria":"7 temps","position":1,"score1":6,"score2":3},
    {"criteria":[1,1,1,6],"position":2,"score1":11,"score2":6},
    {"criteria":[2,2,5],"position":2,"score1":10,"score2":6},
    {"criteria":[3,3,4],"position":2,"score1":12,"score2":7},
    {"criteria":[3,6],"position":2,"score1":8,"score2":4},
    {"criteria":[4,5],"position":2,"score1":9,"score2":5},
    {"criteria":[1,1,1,4],"position":2,"score1":9,"score2":5},
    {"criteria":"two streets all parks","position":2,"score1":7,"score2":4},
    {"criteria":"two streets all pools","position":2,"score1":7,"score2":4},
    {"criteria":["all pools all parks",1],"position":2,"score1":8,"score2":3},
    {"criteria":["all pools all parks",2],"position":2,"score1":10,"score2":5},
    {"criteria":"all pools all parks one roundabout","position":2,"score1":10,"score2":5},
    {"criteria":[1,2,6],"position":3,"score1":12,"score2":7},
    {"criteria":[1,4,5],"position":3,"score1":13,"score2":7},
    {"criteria":[3,4],"position":3,"score1":7,"score2":3},
    {"criteria":[2,5],"position":3,"score1":7,"score2":3},
    {"criteria":[1,2,2,3],"position":3,"score1":11,"score2":6},
    {"criteria":[2,3,5],"position":3,"score1":13,"score2":7}
]

CONSTRUCTION_CARDS = [
    [1,"surveyor"],
    [1,"landscaper"],
    [1,"agent"],
    [2,"surveyor"],
    [2,"landscaper"],
    [2,"agent"],
    [3,"surveyor"],
    [3,"pool"],
    [3,"temp"],
    [3,"bis"],
    [4,"landscaper"],
    [4,"agent"],
    [4,"pool"],
    [4,"temp"],
    [4,"bis"],
    [5,"surveyor"],
    [5,"surveyor"],
    [5,"landscaper"],
    [5,"landscaper"],
    [5,"agent"],
    [5,"agent"],
    [6,"surveyor"],
    [6,"surveyor"],
    [6,"pool"],
    [6,"temp"],
    [6,"bis"],
    [6,"landscaper"],
    [6,"agent"],
    [7,"surveyor"],
    [7,"pool"],
    [7,"temp"],
    [7,"bis"],
    [7,"landscaper"],
    [7,"landscaper"],
    [7,"agent"],
    [7,"agent"],
    [8,"surveyor"],
    [8,"surveyor"],
    [8,"pool"],
    [8,"temp"],
    [8,"bis"],
    [8,"landscaper"],
    [8,"landscaper"],
    [8,"agent"],
    [8,"agent"],
    [9,"surveyor"],
    [9,"pool"],
    [9,"temp"],
    [9,"bis"],
    [9,"landscaper"],
    [9,"landscaper"],
    [9,"agent"],
    [9,"agent"],
    [10,"surveyor"],
    [10,"surveyor"],
    [10,"pool"],
    [10,"temp"],
    [10,"bis"],
    [10,"landscaper"],
    [10,"agent"],
    [11,"surveyor"],
    [11,"surveyor"],
    [11,"landscaper"],
    [11,"landscaper"],
    [11,"agent"],
    [11,"agent"],
    [12,"pool"],
    [12,"temp"],
    [12,"bis"],
    [12,"landscaper"],
    [12,"agent"],
    [13,"landscaper"],
    [13,"pool"],
    [13,"temp"],
    [13,"bis"],
    [14,"surveyor"],
    [14,"landscaper"],
    [14,"agent"],
    [15,"surveyor"],
    [15,"landscaper"],
    [15,"agent"]
]
