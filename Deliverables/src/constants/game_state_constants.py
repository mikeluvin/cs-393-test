from enum import Enum
import json

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
