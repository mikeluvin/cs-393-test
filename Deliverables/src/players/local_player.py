from . import Player
from game_state import GameState
from moves import MoveGenerator
from player_state import PlayerState

class LocalPlayer(Player):
    def __init__(self, name: str, move_generator: MoveGenerator) -> None:
        self._MoveGenerator = move_generator
        super().__init__(name)

    def _get_next_player_state(self, game_state: GameState) -> PlayerState:
        return self._MoveGenerator(game_state, self._player_state)