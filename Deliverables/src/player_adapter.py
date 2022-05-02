import socket
import json
from exception import PlayerAdapterException
from game_state import GameState
from player_state import PlayerState
from generate_move import MoveGenerator

class PlayerAdapter():
    def __init__(self, network_config: dict) -> None:
        # if set(network_config.keys()) != set(["host", "port"]):
        self.host = network_config["host"]
        self.port = network_config["port"]
        self._create_tcp_connection()
        self._play_game()

    def _create_tcp_connection(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.sendall(b"\"team23\"\n")

    def _play_game(self) -> None:
        playing_keys = set(["game-state", "player-state"])
        game_over_keys = set(["game-over"])
        data = ""
        while True:
            data += self.sock.recv(8192).decode("utf-8").strip()
            try:
                request, num_bytes = json.JSONDecoder().raw_decode(data)
            except: # wait for more bytes to arrive
                continue

            #validate requests. Maybe use the JSON schema validator?
            req_keys = set(request.keys()) if type(request) == dict else None
            if req_keys == playing_keys:
                game_state = GameState(request["game-state"])
                player_state = PlayerState(request["player-state"])
                new_player_state = MoveGenerator(game_state, player_state).generate_move()
                self.sock.sendall(bytes(json.dumps(new_player_state.to_dict()) + "\n", "utf-8"))
            elif req_keys == game_over_keys:
                self.sock.sendall(b"\"ack\"\n")
                self.sock.close()
                break
            else:
                raise PlayerAdapterException(f"Received {data}\n\n but request must be a dictionary \
                        containing keys ('game-state', 'player-state'), or 'game-over'.")

            data = data[num_bytes:]
