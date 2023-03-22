from typing import Sequence
from attrs import asdict
from sqlalchemy import Column, Integer, Float, String, ForeignKey, delete, select
from sqlalchemy.orm import relationship
from sqlalchemy.exc import NoResultFound

from ..domain.exception import DomainException
from ..domain.models import Maschine, MaschinenBefaehigung, no_maschinenbefaehigungen


from .database import Base
from sqlalchemy.ext.asyncio import AsyncSession


class MaschineEntity(Base):
    __tablename__ = "maschinen"

    id = Column(String, primary_key=True)
    name = Column(String)
    ruestzeit = Column(Float)
    kosten_minute = Column("kostenMinute", Float)
    ausfall_wahrscheinlichkeit = Column("ausfallWahrscheinlichkeit", Float)
    mitarbeiter_min = Column("mitarbeiterMin", Integer)
    mitarbeiter_max = Column("mitarbeiterMax", Integer)

    maschinenbefaehigungen = relationship(
        "MaschinenBefaehigungEntity",
        lazy="joined",
        cascade="all, delete-orphan",
        back_populates="maschine",
    )


class MaschinenBefaehigungEntity(Base):
    __tablename__ = "maschinenbefaehigung"

    id = Column(String, primary_key=True)
    schritt_id = Column("schrittId", String)
    taktrate = Column(Float)
    maschinen_id = Column(String, ForeignKey("maschinen.id", ondelete="CASCADE"))
    maschine = relationship(
        "MaschineEntity",
        back_populates="maschinenbefaehigungen",
    )


# define persistence interface + implementation here


async def get_maschinen(
    session: AsyncSession, skip: int = 0, take: int = 20
) -> Sequence[Maschine]:
    query = await session.execute(select(MaschineEntity).offset(skip).limit(take))

    return [
        Maschine(
            id=m.id,
            name=m.name,
            ruestzeit=m.ruestzeit,
            kosten_minute=m.kosten_minute,
            ausfall_wahrscheinlichkeit=m.ausfall_wahrscheinlichkeit,
            mitarbeiter_min=m.mitarbeiter_min,
            mitarbeiter_max=m.mitarbeiter_max,
            maschinenbefaehigungen=list(
                [
                    MaschinenBefaehigung(
                        id=mb.id, schritt_id=mb.schritt_id, taktrate=mb.taktrate
                    )
                    for mb in m.maschinenbefaehigungen
                ]
            ),
        )
        for m in query.scalars().unique()
    ]


async def add_maschine(session: AsyncSession, maschine: Maschine) -> Maschine:
    new_maschine = MaschineEntity(
        **asdict(maschine, filter=no_maschinenbefaehigungen),
        maschinenbefaehigungen=[
            MaschinenBefaehigungEntity(**asdict(x))
            for x in maschine.maschinenbefaehigungen
        ],
    )
    session.add(new_maschine)
    await session.commit()
    return maschine


async def remove_maschine(session: AsyncSession, maschine_id: str) -> None:
    row = await session.execute(select(MaschineEntity).where(MaschineEntity.id == maschine_id))
    try:
        row = row.scalar_one()
    except NoResultFound:
        raise DomainException(message=f"Machine with id {maschine_id} not found!")    
    await session.delete(row)
    await session.commit()

