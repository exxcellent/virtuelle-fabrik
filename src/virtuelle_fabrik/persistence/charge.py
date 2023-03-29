from typing import List, Sequence
from attrs import asdict
from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from virtuelle_fabrik.domain.models import Charge, Produktbedarf

from .database import Base

from .produkte import ProduktEntity, convert_to_produkt
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
    produktbedarf: Mapped[List["ProduktbedarfEntity"]] = relationship(lazy="joined")


# define persistence interface + implementation here


def convert_to_charge(entity: ChargeEntity) -> Charge:
    return Charge(
        id=entity.id,
        name=entity.name,
        prioritaet=entity.prioritaet,
        produktbedarf=[
            Produktbedarf(
                id=x.id, produkt=convert_to_produkt(x.produkt), stueckzahl=x.stueckzahl
            )
            for x in entity.produktionsschritte
        ],
    )


async def get_all_chargen(
    session: AsyncSession, skip: int = 0, take: int = 20
) -> Sequence[Charge]:
    query = await session.execute(select(ChargeEntity).offset(skip).limit(take))

    return [convert_to_charge(p) for p in query.scalars().unique().all()]


async def get_charge(session: AsyncSession, charge_id: str) -> Charge:
    query = await session.execute(
        select(ChargeEntity).filter(ChargeEntity.id == charge_id)
    )
    try:
        charge_entity = query.scalars().unique().one()
        return convert_to_charge(charge_entity)
    except NoResultFound:
        raise DomainException(message=f"Charge with id {charge_id} not found!")


async def add_charge(session: AsyncSession, charge: Charge) -> Charge:
    new_charge = ChargeEntity(
        id=charge.id,
        name=charge.name,
        prioritaet=charge.prioritaet,
        produktbedarf=list(
            [
                ProduktbedarfEntity(
                    id=x.id,
                    produkt_id=x.produkt.id,
                    stueckzahl=x.stueckzahl,
                )
                for x in charge.produktbedarf
            ]
        ),
    )

    session.add(new_charge)
    await session.commit()

    return charge


async def remove_charge(session: AsyncSession, charge_id: str) -> None:
    row = await session.execute(
        select(ChargeEntity).where(ChargeEntity.id == charge_id)
    )
    try:
        row = row.unique().scalar_one()
    except NoResultFound:
        raise DomainException(message=f"Charge with id {charge_id} not found!")
    await session.delete(row)
    await session.commit()
