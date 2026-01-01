from enum import UNIQUE, StrEnum, auto, verify


@verify(UNIQUE)
class Environment(StrEnum):
    """Environment the app is running in."""

    local = auto()
    prod = auto()
