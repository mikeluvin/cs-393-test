from . import parse_stdin
from player_adapter import PlayerAdapter
from moves import MoveGenerator

def main():
    input_json = parse_stdin()
    PlayerAdapter(input_json[0], MoveGenerator)

if __name__ == "__main__":
    main()