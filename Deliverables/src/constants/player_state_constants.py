import json
PARK_MAXES = [3, 4, 5]
POOL_LOCS = [[2, 6, 7], [0, 3, 7], [1, 6, 10]]
STREET_LENS = [10, 11, 12]
MAX_REFUSALS = 3

EMPTY_PS = {
    "agents":[0,0,0,0,0,0],
    "city-plan-score":["blank","blank","blank"],
    "refusals":0,
    "streets":[
      {
        "homes":[
          "blank",False,
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False]
        ],
        "parks":0,
        "pools":[False,False,False]
      },
      {
        "homes":[
          "blank",False,
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False]
        ],
        "parks":0,
        "pools":[False,False,False]
      },
      {
        "homes":[
          "blank",False,
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False],
          [False,"blank",False]
        ],
        "parks":0,
        "pools":[False,False,False]
      }
    ],
    "temps":0
}