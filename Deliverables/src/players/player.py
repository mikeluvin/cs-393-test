from game_state import GameState
from player_state import PlayerState
from moves import MoveValidator
from exception import MoveException

class Player():
    def __init__(self, name:str) -> None:
        self._player_state = PlayerState()
        self._name = name
        self.cheated = False

    @property
    def name(self):
        return self._name

    @property
    def player_state(self) -> PlayerState:
        '''
        Returns this player's PlayerState, or False if they cheated.
        '''
        return self._player_state

    @player_state.setter
    def player_state(self, player_state: PlayerState) -> None:
        self._player_state = player_state

    def play_next_move(self, game_state: GameState) -> None:
        '''
        Given a GameState, get the player's next move and update self.player_state
        their new PlayerState, or False if they cheated.
        '''
        new_ps = self._get_next_player_state(game_state)
        if not new_ps:
            self._set_cheater()
            return 

        try:
            MoveValidator(game_state, self._player_state, new_ps).validate_move()
            self._player_state = new_ps
        except MoveException:
            self._set_cheater()

    def _get_next_player_state(self, game_state: GameState):
        '''
        Given a GameState, get the player's new player state. Returns
        their new PlayerState, (or False if they disconnected or sent
        an invalid PlayerState, only possible with the NetworkPlayer).
        '''
        raise NotImplementedError()

    def _set_cheater(self):
        self._player_state = False
        self.cheated = True
        self.close()
    
    def close(self):
        pass

    def send_final_scores(self, scores: dict):
        pass

    def get_score(self, temps_lst: list):
        return self._player_state.calculate_score(temps_lst) if self._player_state else False