import json
from game_state import GameState
from player_state import PlayerState
from . import parse_stdin
from moves import MoveValidator
from exception import MoveException

def main():
    input_json = parse_stdin()
    game_state = GameState(input_json[0][0])
    ps1, ps2 = PlayerState(input_json[0][1]), PlayerState(input_json[0][2])
    move_validator = MoveValidator(game_state, ps1, ps2)
    try:
        move_validator.validate_move()
        valid = True
    except MoveException:
        valid = False

    print(json.dumps(valid))

if __name__ == "__main__":
    main()