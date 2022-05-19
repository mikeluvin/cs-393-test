import socket

from . import Player
from game_state import GameState
from player_state import PlayerState
from exception import PlayerStateException
from network import NetworkAdapter

class NetworkPlayer(Player):
    def __init__(self, sock: socket, addr) -> None:
        self._network = NetworkAdapter(sock)
        self._closed = False
        self._addr = addr
        super().__init__()

    def get_next_move(self, game_state: GameState):
        self._network.send(game_state.to_dict())
        new_ps = self._network.recv()
        try:
            return PlayerState(new_ps)
        # if player sends an invalid PlayerState, they cheated
        except PlayerStateException:
            return False
    
    def close(self):
        if not self._closed:
            self._network.close()
            self._closed = True

    def send_final_scores(self, scores: list):
        self._network.send(scores)
        self.close()
        # do we need to wait for the ack?


    