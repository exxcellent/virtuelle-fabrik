from typing import List
from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from virtuelle_fabrik.persistence.maschinen import MaschineEntity
from virtuelle_fabrik.persistence.produkte import ArbeitsschrittEntity
from virtuelle_fabrik.persistence.produktionslinien import (
    ProduktionslinieEntity,
    StationEntity,
)

from .database import Base


class MaschinenauslastungEntity(Base):
    __tablename__ = "maschinenauslastung"

    id = Column(String, primary_key=True)
    maschine: Mapped[MaschineEntity] = relationship()
    arbeitsschritt: Mapped[ArbeitsschrittEntity] = relationship()
    auslastung = Column(Float, nullable=False)
    leistungsergebnis_id: Mapped[str] = mapped_column(
        ForeignKey("leistungsergebnisse.id")
    )


class LeistungsErgebnisEntity(Base):
    __tablename__ = "leistungsergebnisse"

    id = Column(String, primary_key=True)
    kosten_produkt = Column(Float, nullable=False)
    maschinenauslastungen: Mapped[List[MaschinenauslastungEntity]] = relationship(
        cascade="all, delete-orphan"
    )
    optimierungsergebnis_id: Mapped[str] = mapped_column(
        ForeignKey("optimierungsergebnisse.id")
    )


class OptimierungsErgebnisEntity(Base):
    __tablename__ = "optimierungsergebnisse"

    id = Column(String, primary_key=True)
    station: Mapped[StationEntity] = relationship()
    gegeben: Mapped[LeistungsErgebnisEntity] = relationship(
        cascade="all, delete-orphan"
    )
    gegeben_id: Mapped[str] = mapped_column()
    optimiert: Mapped[LeistungsErgebnisEntity] = relationship(
        cascade="all, delete-orphan"
    )
    optimierung_id: Mapped[str] = mapped_column(ForeignKey("optimierungen.id"))


class OptimierungEntity(Base):
    __tablename__ = "optimierungen"

    id = Column(String, primary_key=True)
    ausfuehrung = Column(DateTime)
    produktionslinie: Mapped[ProduktionslinieEntity] = relationship()
    stationen: Mapped[List[OptimierungsErgebnisEntity]] = relationship(
        cascade="all, delete-orphan"
    )
