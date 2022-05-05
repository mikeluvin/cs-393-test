from . import parse_stdin
from player_adapter import PlayerAdapter

def main():
    input_json = parse_stdin()
    PlayerAdapter(input_json[0])

if __name__ == "__main__":
    main()