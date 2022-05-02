import socket

class PlayerAdapter():
    def __init__(self, network_config: dict) -> None:
        # if set(network_config.keys()) != set(["host", "port"]):
        self.host = network_config["host"]
        self.port = network_config["port"]
        self._create_tcp_connection()

    def _create_tcp_connection(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(b"team23\n")

