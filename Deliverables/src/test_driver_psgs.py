import json
import sys
from player_state import PlayerState
from game_state import GameState
from parse_input import parse_stdin

def main():
    if sys.argv[1] == "player":
        ClassName = PlayerState
    elif sys.argv[1] == "game":
        ClassName = GameState
    else:
        raise Exception("please provide either 'player' or 'game' as a command line argument.")

    input_json = parse_stdin()[0]
    try:
        state = ClassName(input_json).to_dict()
    except:
        state = False

    print(json.dumps(state))

if __name__ == "__main__":
    main()