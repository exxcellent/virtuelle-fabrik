from typing import List, Sequence
from attrs import asdict
from sqlalchemy import Column, Integer, Float, String, ForeignKey, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .database import Base

from ..domain.exception import DomainException
from ..domain.models import (
    Material,
    Materialbedarf,
    Produkt,
    Produktionsschritt,
    produkt_without_relationships,
)


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
    material: Mapped["MaterialEntity"] = relationship(lazy="joined")
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
    produktionsschritte: Mapped[List["ProduktionsschrittEntity"]] = relationship(
        lazy="joined"
    )
    materialbedarf: Mapped[List["MaterialbedarfEntity"]] = relationship(lazy="joined")


# define persistence interface + implementation here


async def get_all_material(
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


async def get_material(session: AsyncSession, material_id: str) -> Material:
    query = await session.execute(
        select(MaterialEntity).filter(MaterialEntity.id == material_id)
    )
    try:
        m = query.scalars().one()
        await session.commit()
        return Material(
            id=m.id,
            name=m.name,
            kosten_stueck=m.kosten_stueck,
            bestand=m.bestand,
            aufstocken_minute=m.aufstocken_minute,
        )
    except NoResultFound:
        raise DomainException(message=f"Material with id {material_id} not found!")


async def add_material(session: AsyncSession, material: Material) -> Material:
    new_material = MaterialEntity(
        **asdict(material),
    )
    session.add(new_material)
    await session.commit()
    return material


async def remove_material(session: AsyncSession, material_id: str) -> None:
    row = await session.execute(
        select(MaterialEntity).where(MaterialEntity.id == material_id)
    )
    try:
        row = row.unique().scalar_one()
    except NoResultFound:
        raise DomainException(message=f"Material with id {material_id} not found!")
    await session.delete(row)
    await session.commit()


def convert_to_produkt(entity: ProduktEntity) -> Produkt:
    return Produkt(
        id=entity.id,
        name=entity.name,
        verkaufspreis=entity.verkaufspreis,
        produktionsschritte=[
            Produktionsschritt(id=x.id, schritt=x.schritt)
            for x in entity.produktionsschritte
        ],
        materialbedarf=[
            Materialbedarf(
                id=x.id,
                material=Material(
                    id=x.material.id,
                    name=x.material.name,
                    kosten_stueck=x.material.kosten_stueck,
                    bestand=x.material.bestand,
                    aufstocken_minute=x.material.aufstocken_minute,
                ),
                menge=x.menge,
            )
            for x in entity.materialbedarf
        ],
    )


async def get_all_produkte(
    session: AsyncSession, skip: int = 0, take: int = 20
) -> Sequence[Produkt]:
    query = await session.execute(select(ProduktEntity).offset(skip).limit(take))

    return [convert_to_produkt(p) for p in query.scalars().unique().all()]


async def get_produkt(session: AsyncSession, produkt_id: str) -> Produkt:
    query = await session.execute(
        select(ProduktEntity).filter(ProduktEntity.id == produkt_id)
    )
    try:
        product_entity = query.scalars().unique().one()
        await session.commit()
        return convert_to_produkt(product_entity)
    except NoResultFound:
        raise DomainException(message=f"Produkt with id {produkt_id} not found!")


async def add_produkt(session: AsyncSession, produkt: Produkt) -> Produkt:
    new_produkt = ProduktEntity(
        **asdict(produkt, filter=produkt_without_relationships),
        produktionsschritte=[
            ProduktionsschrittEntity(**asdict(x)) for x in produkt.produktionsschritte
        ],
        materialbedarf=[
            MaterialbedarfEntity(id=x.id, menge=x.menge, material_id=x.material.id)
            for x in produkt.materialbedarf
        ],
    )
    session.add(new_produkt)
    await session.commit()
    return produkt
