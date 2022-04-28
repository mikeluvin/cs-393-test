import json
from game_state import GameState
from player_state import PlayerState
from parse_input import parse_stdin
from generate_move import MoveGenerator

def main():
    input_json = parse_stdin()
    game_state = GameState(input_json[0][0])
    player_state = PlayerState(input_json[0][1])
    move_generator = MoveGenerator(game_state, player_state)
    new_player_st = move_generator.generate_move()

    print(json.dumps(new_player_st.to_dict()))

if __name__ == "__main__":
    main()