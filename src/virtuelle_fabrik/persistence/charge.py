from typing import List, Sequence
from attrs import asdict
from sqlalchemy import Column, Integer, Float, String, ForeignKey, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .database import Base

from .produkte import ProduktEntity
from virtuelle_fabrik.domain.exception import DomainException


class ProduktbedarfEntity(Base):
    __tablename__ = "produktbedarf"

    id = Column(String, primary_key=True)
    produkt_id: Mapped[str] = mapped_column(ForeignKey("produkt.id"))
    produkt: Mapped["ProduktEntity"] = relationship(lazy="joined")
    stueckzahl = Column(Integer)
    charge_id: Mapped[str] = mapped_column(ForeignKey("charge.id"))



class ChargeEntity(Base):
    __tablename__ = "charge"

    id = Column(String, primary_key=True)
    name = Column(String)
    prioritaet = Column(Integer)
    produktbedarf: Mapped[List["ProduktbedarfEntity"]] = relationship(
        lazy="joined"
    )
