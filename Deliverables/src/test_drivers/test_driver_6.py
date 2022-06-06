from . import parse_stdin
from player_client import PlayerClient
from moves import SimpleMoveGenerator, SmartMoveGenerator

def main():
    input_json = parse_stdin()
    client = PlayerClient(input_json[0], SmartMoveGenerator)
    client.play_game()

if __name__ == "__main__":
    main()