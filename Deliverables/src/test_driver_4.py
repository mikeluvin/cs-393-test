import json
from game_state import GameState
from player_state import PlayerState
from parse_input import parse_stdin
from validate_move import MoveValidator

def main():
    input_json = parse_stdin()
    game_state = GameState(input_json[0][0])
    ps1, ps2 = PlayerState(input_json[0][1]), PlayerState(input_json[0][2])
    move_validator = MoveValidator(game_state, ps1, ps2)
    valid = move_validator.validate_move()

    print(json.dumps(valid))

if __name__ == "__main__":
    main()