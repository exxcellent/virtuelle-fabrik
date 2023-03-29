from typing import List, Sequence
from attrs import asdict
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .database import Base

from virtuelle_fabrik.domain.exception import DomainException
from virtuelle_fabrik.domain.models import (
    Arbeitsschritt,
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
    produkt_id: Mapped[str] = mapped_column(
        ForeignKey("produkt.id", ondelete="CASCADE")
    )


class ArbeitsschrittEntity(Base):
    __tablename__ = "arbeitsschritt"

    id = Column(String, primary_key=True)
    name = Column(String)


class ProduktionsschrittEntity(Base):
    __tablename__ = "produktionsschritt"

    id = Column(String, primary_key=True)
    schritt = Column(Integer)
    arbeitsschritt_id: Mapped[str] = mapped_column(ForeignKey("arbeitsschritt.id"))
    arbeitsschritt: Mapped[ArbeitsschrittEntity] = relationship(lazy="joined")
    produkt_id: Mapped[str] = mapped_column(
        ForeignKey("produkt.id", ondelete="CASCADE")
    )


class ProduktEntity(Base):
    __tablename__ = "produkt"

    id = Column(String, primary_key=True)
    name = Column(String)
    verkaufspreis = Column(Float)
    produktionsschritte: Mapped[List["ProduktionsschrittEntity"]] = relationship(
        lazy="joined",
        cascade="all, delete-orphan",
    )
    materialbedarf: Mapped[List["MaterialbedarfEntity"]] = relationship(
        lazy="joined",
        cascade="all, delete-orphan",
    )


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


async def get_arbeitsschritte(
    session: AsyncSession, skip: int = 0, take: int = 20
) -> Sequence[Arbeitsschritt]:
    query = await session.execute(select(ArbeitsschrittEntity).offset(skip).limit(take))

    return [
        Arbeitsschritt(
            id=entity.id,
            name=entity.name,
        )
        for entity in query.scalars().all()
    ]


async def get_arbeitsschritt(
    session: AsyncSession, arbeitsschritt_id: str
) -> Arbeitsschritt:
    query = await session.execute(
        select(ArbeitsschrittEntity).filter(
            ArbeitsschrittEntity.id == arbeitsschritt_id
        )
    )
    try:
        entity = query.scalars().one()
        return Arbeitsschritt(
            id=entity.id,
            name=entity.name,
        )
    except NoResultFound:
        raise DomainException(
            message=f"Arbeitsschritt with id {arbeitsschritt_id} not found!"
        )


async def add_arbeitsschritt(
    session: AsyncSession, arbeitsschritt: Arbeitsschritt
) -> Arbeitsschritt:
    new_arbeitsschritt = ArbeitsschrittEntity(
        **asdict(arbeitsschritt),
    )
    session.add(new_arbeitsschritt)
    await session.commit()
    return arbeitsschritt


async def remove_arbeitsschritt(session: AsyncSession, arbeitsschritt_id: str) -> None:
    row = await session.execute(
        select(ArbeitsschrittEntity).where(ArbeitsschrittEntity.id == arbeitsschritt_id)
    )
    try:
        row = row.unique().scalar_one()
    except NoResultFound:
        raise DomainException(
            message=f"Arbeitsschritt with id {arbeitsschritt_id} not found!"
        )
    await session.delete(row)
    await session.commit()


def convert_to_produkt(entity: ProduktEntity) -> Produkt:
    return Produkt(
        id=entity.id,
        name=entity.name,
        verkaufspreis=entity.verkaufspreis,
        produktionsschritte=[
            Produktionsschritt(
                id=x.id,
                schritt=x.schritt,
                arbeitsschritt=Arbeitsschritt(
                    id=x.arbeitsschritt.id, name=x.arbeitsschritt.name
                ),
            )
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
        return convert_to_produkt(product_entity)
    except NoResultFound:
        raise DomainException(message=f"Produkt with id {produkt_id} not found!")


async def add_produkt(session: AsyncSession, produkt: Produkt) -> Produkt:
    new_produkt = ProduktEntity(
        **asdict(produkt, filter=produkt_without_relationships),
        produktionsschritte=[
            ProduktionsschrittEntity(
                id=x.id, schritt=x.schritt, arbeitsschritt_id=x.arbeitsschritt.id
            )
            for x in produkt.produktionsschritte
        ],
        materialbedarf=[
            MaterialbedarfEntity(id=x.id, menge=x.menge, material_id=x.material.id)
            for x in produkt.materialbedarf
        ],
    )
    session.add(new_produkt)
    await session.commit()
    return produkt

async def remove_produkt(session: AsyncSession, produkt_id: str) -> None:
    row = await session.execute(
        select(ProduktEntity).where(ProduktEntity.id == produkt_id)
    )
    try:
        row = row.unique().scalar_one()
    except NoResultFound:
        raise DomainException(message=f"Produkt with id {produkt_id} not found!")
    await session.delete(row)
    await session.commit()