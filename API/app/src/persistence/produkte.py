from typing import List
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base


class MaterialEntity(Base):
    __tablename__ = "material"

    id = Column(String, primary_key=True)
    name = Column(String)
    kosten_stueck = Column("kostenStueck", Float)
    bestand = Column(Float)
    aufstocken_minute = Column("aufstockenMinute", Float)


class MaterialbedarfEntity(Base):
    __tablename__ = "materialbedarf"

    id = Column(String, primary_key=True)
    menge = Column(Float)
    material_id: Mapped[str] = mapped_column(ForeignKey("material.id"))
    material: Mapped["MaterialEntity"] = relationship()
    produkt_id: Mapped[str] = mapped_column(ForeignKey("produkt.id"))


class ProduktionsschrittEntity(Base):
    __tablename__ = "produktionsschritt"

    id = Column(String, primary_key=True)
    schritt = Column(Integer)
    produkt_id: Mapped[str] = mapped_column(ForeignKey("produkt.id"))


class ProduktEntity(Base):
    __tablename__ = "produkt"

    id = Column(String, primary_key=True)
    name = Column(String)
    verkaufspreis = Column(Float)
    produktionsschritte: Mapped[List["ProduktionsschrittEntity"]] = relationship()
    materialbedarf: Mapped[List["MaterialbedarfEntity"]] = relationship()


