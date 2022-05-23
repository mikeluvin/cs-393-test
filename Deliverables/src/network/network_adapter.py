import socket
import json

from exception import PlayerConnectionException

ENCODING = "utf-8"

class NetworkAdapter():
    def __init__(self, sock: socket):
        self._sock = sock
        self._data = b""

    def send(self, msg: str):
        self._sock.sendall(f"{ json.dumps(msg) }\n".encode())

    def recv(self) -> str:
        curr_data, data_lst = b"", []
        while b"\n" not in curr_data:
            curr_data = self._sock.recv(8192)
            if len(curr_data) == 0:
                raise PlayerConnectionException()
            data_lst.append(curr_data)

        self._data += b"".join(data_lst)
        decoded_data_lst = self._data.decode(ENCODING).split("\n", maxsplit=1)
        request = decoded_data_lst[0].strip()
        # if we somehow have >2 valid json objects, keep the remaining
        # so we can access them in the future
        self._data = decoded_data_lst[1].encode(ENCODING)
        
        return json.loads(request)

    def close(self) -> None:
        self._sock.close()