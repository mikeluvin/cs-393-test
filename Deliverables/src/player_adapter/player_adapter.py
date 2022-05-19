import socket
import json
from exception import PlayerAdapterException
from game_state import GameState
from player_state import PlayerState
from moves import MoveGenerator
from network import NetworkAdapter

class PlayerAdapter():
    def __init__(self, network_config: dict, Player: MoveGenerator) -> None:
        if set(network_config.keys()) != set(["host", "port"]):
            return PlayerAdapterException(f"Received {network_config}\n\n, but expected a dictionary \
                    with keys 'host' and 'port-number'.")
        self._host = network_config["host"]
        self._port = network_config["port"]
        self._Player = Player
        self._data = b""
        self._create_tcp_connection()
        self._play_game()

    def _create_tcp_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._host, self._port))
        self._network = NetworkAdapter(sock)

    def _play_game(self) -> None:
        playing_keys = set(["game-state", "player-state"])
        game_over_keys = set(["game-over"])
        self._network.send("team23")

        while True:
            request = self._network.recv()
            req_keys = set(request.keys()) if type(request) == dict else None
            if req_keys == playing_keys:
                self._play_move(request)
            elif req_keys == game_over_keys:
                self._end_game()
                break
            else:
                raise PlayerAdapterException(f"Received {request}\n\n but request must be a dictionary \
                        with keys ('game-state', 'player-state'), or 'game-over'.")

    def _play_move(self, request: dict) -> None:
        game_state = GameState(request["game-state"])
        player_state = PlayerState(request["player-state"])
        new_player_state = self._Player(game_state, player_state).generate_move()
        self._network.send(new_player_state.to_dict())

    def _end_game(self):
        self._network.send("ack")
        self._network.close()
