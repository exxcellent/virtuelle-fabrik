

from attr import define


@define
class MaschinenBefaehigung:
    id: str
    schritt_id: str
    taktrate: float

@define
class Maschine:
    id: str
    name: str
    ruestzeit: float
    kosten_minute: float
    ausfall_wahrscheinlichkeit: float
    mitarbeiter_min: int
    mitarbeiter_max: int
    maschinenbefaehigungen: list[MaschinenBefaehigung]


def no_maschinenbefaehigungen(a, _):
    return a.name != ("maschinenbefaehigungen")