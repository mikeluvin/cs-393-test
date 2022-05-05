from exception import *
from helpers import *

class Effect():
    def __init__(self, effect: str) -> None:
        self._effects = set(["surveyor", "agent", "landscaper", "pool", "temp", "bis"])
        self.effect = effect

    @property
    def effect(self) -> str:
        return self._effect

    @effect.setter
    def effect(self, effect: str) -> None:
        if not check_type_and_membership(effect, str, self._effects):
            raise EffectException(f"Given {effect}, but effect must be one of {self._effects}.")
        self._effect = effect

    def __repr__(self) -> str:
        return self._effect

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)