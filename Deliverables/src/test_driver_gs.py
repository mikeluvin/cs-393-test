import json
from game_state import GameState
from parse_input import parse_stdin

def main():
    input_json = parse_stdin()[0]
    try:
        game_state = GameState(input_json).to_dict()
    except:
        game_state = False

    print(json.dumps(game_state))

if __name__ == "__main__":
    main()