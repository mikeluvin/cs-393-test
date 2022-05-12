# valid city plan positions are 1, 2, or 3
VALID_POSNS = set(range(1, 4))

CRITERIA_CARDS = [
    [
        [ "all houses", 0 ],
        [ "all houses", 2 ],
        "end houses",
        "7 temps",
        "5 bis"
    ],
    [
        "two streets all parks",
        "two streets all pools",
        [ "all pools all parks", 1 ],
        [ "all pools all parks", 2 ],
        "all pools all parks one roundabout"
    ]
]
