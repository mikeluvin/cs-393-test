import json
import sys
from game_state import GameState
from player_state import PlayerState
from parse_input import parse_stdin
from generate_move import MoveGenerator

def main():
    input_json = parse_stdin()
    if sys.argv[1] == "generate":
        game_state = GameState(input_json[0][0])
        player_state = PlayerState(input_json[0][1])
        move_generator = MoveGenerator(game_state, player_state)
        new_player_st = move_generator.generate_move()
        sys.stdout.write(json.dumps(new_player_st.to_dict()))
    elif sys.argv[1] == "score":
        player_state = PlayerState(input_json[0][0])
        temps_lst = input_json[0][1]
        sys.stdout.write(json.dumps(player_state.calculate_score(temps_lst)))


if __name__ == "__main__":
    main()