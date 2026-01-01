from enum import UNIQUE, StrEnum, auto, verify


@verify(UNIQUE)
class RouteMap(StrEnum):
    GOOGLE_CALLBACK = auto()
    HEALTHZ = auto()
