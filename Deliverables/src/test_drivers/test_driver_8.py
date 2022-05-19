from . import parse_stdin
from game_server import GameServer
from constants import CITY_PLAN_CARDS, CONSTRUCTION_CARDS

def main():
    input_json = parse_stdin()
    GameServer(input_json[0], [], CONSTRUCTION_CARDS, CITY_PLAN_CARDS)

if __name__ == "__main__":
    main()