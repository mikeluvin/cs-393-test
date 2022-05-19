import socket

HOST = "127.0.0.1"

class GameServer():
    def __init__(self, game_config: dict, cc_lst: list, cp_lst: list) -> None:
        self._num_players = game_config["players"]
        self._port = game_config["port"]
        self._player_names = []

    def _start_tcp_listener(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.listen()
        