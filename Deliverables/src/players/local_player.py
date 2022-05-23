from . import Player
from game_state import GameState
from moves import MoveGenerator

class LocalPlayer(Player):
    def __init__(self, name: str, move_generator: MoveGenerator) -> None:
        self._MoveGenerator = move_generator
        super().__init__(name)

    def get_next_move(self, game_state: GameState):
        return self._MoveGenerator(game_state, self._player_state)