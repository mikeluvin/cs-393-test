from typing import *

def my_assert(to_assert: bool, Exn: Exception, message: str) -> None:
    '''
    Asserts that to_assert is True, raises Exception Exn otherwise.
    '''
    if not to_assert:
        raise Exn(message)

class WelcomeToException(Exception):
    '''
    Base class for all exceptions related to Welcome To.
    '''
    def __init__(self, message="Exception raised in Welcome To."):
        super().__init__(message)


class PlayerStateException(WelcomeToException):
    '''
    Base class for all exceptions related to the PlayerState.
    '''
    def __init__(self, message="Invalid player state."):
        super().__init__(message)

class HomeException(PlayerStateException):
    def __init__(self, message="Invalid home."):
        super().__init__(message)

class StreetException(PlayerStateException):
    def __init__(self, message="Invalid street."):
        super().__init__(message)


class GameStateException(WelcomeToException):
    '''
    Base class for all exceptions related to the GameState.
    '''
    def __init__(self, message="Invalid game state."):
        super().__init__(message)

class CityPlanException(GameStateException):
    def __init__(self, message="Invalid city plan."):
        super().__init__(message)

class CriteriaException(CityPlanException):
    def __init__(self, message="Invalid criteria."):
        super().__init__(message)

class ConstructionCardException(GameStateException):
    def __init__(self, message="Invalid construction card."):
        super().__init__(message)

class EffectException(ConstructionCardException):
    def __init__(self, message="Invalid effect."):
        super().__init__(message)


class MoveException(WelcomeToException):
    def __init__(self, message="Invalid move."):
        super().__init__(message)

class PlayerClientException(WelcomeToException):
    def __init__(self, message="Invalid network request."):
        super().__init__(message)

class PlayerConnectionException(WelcomeToException):
    def __init__(self, message="Network connection dropped by player."):
        super().__init__(message)

class CardDeckException(WelcomeToException):
    def __init__(self, message="Invalid card deck."):
        super().__init__(message)