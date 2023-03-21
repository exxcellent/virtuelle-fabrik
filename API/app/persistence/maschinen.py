from typing import Sequence
import uuid
from sqlalchemy import Column, Integer, Float, String, ForeignKey, select
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.ext.asyncio import AsyncSession


class Maschine(Base):
    __tablename__ = "maschinen"

    id = Column(String, primary_key=True)
    name = Column(String)
    ruestzeit = Column(Float)
    kostenMinute = Column(Float)
    ausfallWahrscheinlichkeit = Column(Float)
    mitarbeiterMin = Column(Integer)
    mitarbeiterMax = Column(Integer)

    maschinenbefaehigungen = relationship(
        "MaschinenBefaehigung", back_populates="maschine"
    )


class MaschinenBefaehigung(Base):
    __tablename__ = "maschinenbefaehigung"

    id = Column(String, primary_key=True)
    schrittId = Column(String)
    taktrate = Column(Float)
    maschinen_id = Column(Integer, ForeignKey("maschinen.id"))
    maschine = relationship("Maschine", back_populates="maschinenbefaehigungen")


# define persistence interface + implementation here


async def get_maschinen(
    session: AsyncSession, skip: int = 0, take: int = 20
) -> Sequence[Maschine]:
    query = await session.execute(select(Maschine).offset(skip).limit(take))
    return query.scalars().all()


async def add_maschine(session: AsyncSession, maschine: Maschine) -> Maschine:
    new_maschine = Maschine(
        id=uuid.uuid4().hex,
        name=maschine.name,
        ruestzeit=maschine.ruestzeit,
        kostenMinute=maschine.kostenMinute,
        ausfallWahrscheinlichkeit=maschine.ausfallWahrscheinlichkeit,
        mitarbeiterMin=maschine.mitarbeiterMin,
        mitarbeiterMax=maschine.mitarbeiterMax,
    )
    session.add(new_maschine)
    await session.flush()
    return new_maschine

    # query = maschinen.insert().values(**maschine)
    # machine_id = await database.execute(query)
    # await database.execute(
    #     maschinenbefaehigung.insert().values(
    #         [{"maschinen.id": machine_id, **x} for x in maschine.maschinenbefaehigung]
    #     )
    # )
    # return {**maschine.dict(), "id": machine_id}
