from typing import List, Sequence
from sqlalchemy import Column, String, ForeignKey, Table, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .database import Base
from .maschinen import MaschineEntity, convert_to_maschine, get_maschine
from .charge import ChargeEntity, convert_to_charge, get_charge

from virtuelle_fabrik.domain.models import Produktionslinie, Station
from virtuelle_fabrik.domain.exception import DomainException

station_maschine_association_table = Table(
    "station_maschine_association_table",
    Base.metadata,
    Column("station_id", ForeignKey("stationen.id"), primary_key=True),
    Column("maschine_id", ForeignKey("maschinen.id"), primary_key=True),
)

station_charge_association_table = Table(
    "station_charge_association_table",
    Base.metadata,
    Column("station_id", ForeignKey("stationen.id"), primary_key=True),
    Column("charge_id", ForeignKey("charge.id"), primary_key=True),
)


class StationEntity(Base):
    __tablename__ = "stationen"

    id = Column(String, primary_key=True)
    name = Column(String)
    maschinen: Mapped[List["MaschineEntity"]] = relationship(
        secondary=station_maschine_association_table
    )
    chargen: Mapped[List["ChargeEntity"]] = relationship(
        secondary=station_charge_association_table
    )
    produktionslinie_id: Mapped[str] = mapped_column(ForeignKey("produktionslinien.id"))


class ProduktionslinieEntity(Base):
    __tablename__ = "produktionslinien"

    id = Column(String, primary_key=True)
    stationen: Mapped[List["StationEntity"]] = relationship(lazy="joined")


# define persistence interface + implementation here


def convert_to_station(entity: StationEntity) -> Station:
    return Station(
        id=entity.id,
        name=entity.name,
        maschinen=list([convert_to_maschine(x) for x in entity.maschinen]),
        chargen=list([convert_to_charge(x) for x in entity.chargen]),
    )


async def get_all_stationen(
    session: AsyncSession, skip: int = 0, take: int = 20
) -> Sequence[Station]:
    query = await session.execute(select(StationEntity).offset(skip).limit(take))

    return [convert_to_station(p) for p in query.scalars().unique().all()]


async def get_station(session: AsyncSession, station_id: str) -> Station:
    query = await session.execute(
        select(StationEntity).filter(StationEntity.id == station_id)
    )
    try:
        station_entity = query.scalars().unique().one()
        await session.commit()
        return convert_to_station(station_entity)
    except NoResultFound:
        raise DomainException(message=f"Station with id {station_id} not found!")


async def add_station(session: AsyncSession, station: Station) -> Station:
    new_station = StationEntity(
        id=station.id,
        name=station.name,
        maschinen=list([get_maschine(session, x.id) for x in station.maschinen]),
        chargen=list([get_charge(session, x.id) for x in station.chargen]),
    )

    session.add(new_station)
    await session.commit()

    return station


async def remove_station(session: AsyncSession, station_id: str) -> None:
    row = await session.execute(
        select(StationEntity).where(StationEntity.id == station_id)
    )
    try:
        row = row.unique().scalar_one()
    except NoResultFound:
        raise DomainException(message=f"Station with id {station_id} not found!")
    await session.delete(row)
    await session.commit()


async def get_produktionslinie(
    session: AsyncSession, produktionslinie_id: str
) -> Produktionslinie:
    query = await session.execute(
        select(ProduktionslinieEntity).filter(
            ProduktionslinieEntity.id == produktionslinie_id
        )
    )
    try:
        produktionslinie_entity = query.scalars().unique().one()
        await session.commit()
        return Produktionslinie(
            id=produktionslinie_entity.id,
            stationen=list(
                [
                    Station(
                        id=x.id,
                        name=x.name,
                        maschinen=list([convert_to_maschine(m) for m in x.maschinen]),
                        chargen=list([convert_to_charge(c) for c in x.chargen]),
                    )
                    for x in produktionslinie_entity.stationen
                ]
            ),
        )
    except NoResultFound:
        raise DomainException(
            message=f"Produktionslinie with id {produktionslinie_id} not found!"
        )


async def add_produktionslinie(
    session: AsyncSession, produktionslinie: Produktionslinie
) -> Produktionslinie:
    new_produktionslinie = ProduktionslinieEntity(
        id=produktionslinie.id,
        name=produktionslinie.name,
        maschinen=list(
            [get_maschine(session, x.id) for x in produktionslinie.maschinen]
        ),
        chargen=list([get_charge(session, x.id) for x in produktionslinie.chargen]),
    )
    session.add(new_produktionslinie)
    await session.commit()
    return produktionslinie


async def update_produktionslinie(
    session: AsyncSession, produktionslinie_id, produktionslinie: Produktionslinie
) -> Produktionslinie:
    produktionslinie_entity = await get_produktionslinie(session, produktionslinie_id)

    produktionslinie_entity.name = produktionslinie.name
    produktionslinie_entity.maschinen = list(
        [get_maschine(session, x.id) for x in produktionslinie.maschinen]
    )
    produktionslinie_entity.chargen = list(
        [get_charge(session, x.id) for x in produktionslinie.chargen]
    )

    await session.commit()
    return produktionslinie
