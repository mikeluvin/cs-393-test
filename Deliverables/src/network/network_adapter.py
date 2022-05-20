import socket
import json

from exception import PlayerConnectionException

class NetworkAdapter():
    def __init__(self, sock: socket):
        self._sock = sock
        self._data = b""

    def send(self, msg: str):
        self._sock.sendall(f"{ json.dumps(msg) }\n".encode())

    def recv(self) -> str:
        while b"\n" not in self._data:
            self._data += self._sock.recv(8192)
            if not self._data:
                raise PlayerConnectionException()

        decoded_data_lst = self._data.decode("utf-8").split("\n", maxsplit=1)
        request = decoded_data_lst[0].strip()
        # if we somehow have >2 valid json objects, join the remaining with a "\n"
        # so we can access them in the future
        self._data = "\n".join(decoded_data_lst[1:]).encode("utf-8")
        
        return json.loads(request)

    def close(self) -> None:
        self._sock.close()