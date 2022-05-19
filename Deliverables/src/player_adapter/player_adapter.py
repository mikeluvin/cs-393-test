import socket
import json
from exception import PlayerAdapterException
from game_state import GameState
from player_state import PlayerState
from moves import MoveGenerator

class PlayerAdapter():
    def __init__(self, network_config: dict, Player: MoveGenerator) -> None:
        if set(network_config.keys()) != set(["host", "port"]):
            return PlayerAdapterException(f"Received {network_config}\n\n, but expected a dictionary \
                    with keys 'host' and 'port-number'.")
        self.host = network_config["host"]
        self.port = network_config["port"]
        self.Player = Player
        self.data = b""
        self._create_tcp_connection()
        self._play_game()

    def _create_tcp_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def _send(self, msg: str):
        self.sock.send(f"{json.dumps(msg)}\n".encode())

    def _recv(self) -> str:
        while b"\n" not in self.data:
            self.data += self.sock.recv(8192)

        decoded_data_lst = self.data.decode("utf-8").split("\n", maxsplit=1)
        request = decoded_data_lst[0]
        # if we somehow have >2 valid json objects, join the remaining with a "\n"
        # so we can access them in the future
        self.data = "\n".join(decoded_data_lst[1:]).encode("utf-8") if len(decoded_data_lst) > 1 else b""
        
        return json.loads(request)

    def _play_game(self) -> None:
        playing_keys = set(["game-state", "player-state"])
        game_over_keys = set(["game-over"])
        self._send("team23")

        while True:
            request = self._recv()
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
        new_player_state = self.Player(game_state, player_state).generate_move()
        self._send(new_player_state.to_dict())

    def _end_game(self):
        self._send("ack")
        self.sock.close()
