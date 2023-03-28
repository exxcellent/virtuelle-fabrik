from typing import List
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
    maschinenbefaehigungen: List[MaschinenBefaehigung]


def no_maschinenbefaehigungen(a, _):
    return a.name != ("maschinenbefaehigungen")


@define
class Material:
  id: str
  name: str
  kosten_stueck: float
  bestand: float
  aufstocken_minute: float

@define
class Materialbedarf:
  id: str
  material: Material
  menge: float

@define
class Produktionsschritt:
  id: str
  schritt: int

@define
class Produkt:
  id: str
  name: str
  verkaufspreis: float
  produktionsschritte: List[Produktionsschritt]
  materialbedarf: List[Materialbedarf]


def produkt_without_relationships(a, _):
    return a.name not in set(("produktionsschritte", "materialbedarf"))


@define
class Produktbedarf:
  id: str
  produkt: Produkt
  stueckzahl: int

@define
class Charge:
  id: str
  name: str
  prioritaet: int
  produktbedarf: List[Produktbedarf]

@define
class Station:
  id: str
  name: str
  maschinen: List[Maschine]
  chargen: List[Charge]

@define
class Produktionslinie:
  id: str
  stationen: List[Station]

