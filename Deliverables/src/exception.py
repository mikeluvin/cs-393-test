class HomeException(Exception):
    def __init__(self, message="Invalid home."):
        super().__init__(message)

class StreetException(Exception):
    def __init__(self, message="Invalid street."):
        super().__init__(message)

class PlayerStateException(Exception):
    def __init__(self, message="Invalid player state."):
        super().__init__(message)

class CityPlanException(Exception):
    def __init__(self, message="Invalid city plan."):
        super().__init__(message)

class ConstructionCardException(Exception):
    def __init__(self, message="Invalid construction card."):
        super().__init__(message)

class GameStateException(Exception):
    def __init__(self, message="Invalid game state."):
        super().__init__(message)