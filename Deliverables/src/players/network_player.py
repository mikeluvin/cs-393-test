import socket

from . import Player
from game_state import GameState
from player_state import PlayerState
from exception import PlayerStateException, PlayerConnectionException
from network import NetworkAdapter

class NetworkPlayer(Player):
    def __init__(self, sock: socket, addr) -> None:
        self._network = NetworkAdapter(sock)
        self._closed = False
        self._addr = addr
        self.name = self._network.recv()
        super().__init__()

    def get_next_move(self, game_state: GameState):
        self._network.send({
            "game-state": game_state.to_dict(), 
            "player-state": self._player_state.to_dict()
        })
        try:
            new_ps = self._network.recv()
        except PlayerConnectionException:
            self.close()
            return False

        try:
            return PlayerState(new_ps)
        # if player sends an invalid PlayerState, they cheated
        except PlayerStateException:
            return False
    
    def close(self):
        if not self._closed:
            self._network.close()
            self._closed = True

    def send_final_scores(self, scores: dict):
        if not self._closed:
            self._network.send(scores)
            # wait for the ack
            try:
                self._network.recv()
            except PlayerConnectionException:
                # if the player disconnected, we're closing anyways
                pass

            self.close()


    