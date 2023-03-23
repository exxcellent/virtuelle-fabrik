from typing import List, Sequence
from attrs import asdict
from sqlalchemy import Column, Integer, Float, String, ForeignKey, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .database import Base

from ..domain.exception import DomainException
from ..domain.models import Material


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


# define persistence interface + implementation here


async def get_material(
    session: AsyncSession, skip: int = 0, take: int = 20
) -> Sequence[Material]:
    query = await session.execute(select(MaterialEntity).offset(skip).limit(take))

    return [
        Material(
            id=m.id,
            name=m.name,
            kosten_stueck=m.kosten_stueck,
            bestand=m.bestand,
            aufstocken_minute=m.aufstocken_minute,
        )
        for m in query.scalars().all()
    ]

async def add_material(session: AsyncSession, material: Material) -> Material:
    new_material = MaterialEntity(
        **asdict(material),
    )
    session.add(new_material)
    await session.commit()
    return material


async def remove_material(session: AsyncSession, material_id: str) -> None:
    row = await session.execute(select(MaterialEntity).where(MaterialEntity.id == material_id))
    try:
        row = row.unique().scalar_one()
    except NoResultFound:
        raise DomainException(message=f"Material with id {material_id} not found!")    
    await session.delete(row)
    await session.commit()

