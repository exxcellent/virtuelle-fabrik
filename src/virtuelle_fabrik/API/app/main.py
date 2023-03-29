from typing import List
import uuid
from attrs import asdict


from fastapi.responses import JSONResponse
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseConfig, BaseModel

from virtuelle_fabrik.domain.exception import DomainException
from virtuelle_fabrik.domain.models import (
    Charge,
    Maschine,
    MaschinenBefaehigung,
    Material,
    Materialbedarf,
    Produkt,
    Produktbedarf,
    Produktionsschritt,
)
from virtuelle_fabrik.persistence.charge import add_charge, get_all_chargen, get_charge
from virtuelle_fabrik.persistence.database import async_session
from virtuelle_fabrik.persistence.maschinen import (
    get_maschine,
    get_maschinen,
    add_maschine,
    remove_maschine,
)
from virtuelle_fabrik.persistence.produkte import (
    add_material,
    add_produkt,
    get_all_material,
    get_all_produkte,
    get_material,
    get_produkt,
    remove_material,
)
from .socket_handlers import setupWebsocket


app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setupWebsocket(app)

szenario_router = APIRouter(prefix="/api/szenarios/{szenario_id}")


def to_lower_camel(string: str) -> str:
    upper = "".join(word.capitalize() for word in string.split("_"))
    return upper[:1].lower() + upper[1:]


class APIModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        allow_population_by_field_name = True
        alias_generator = to_lower_camel


class MaschinenBefaehigungIn(APIModel):
    schritt_id: str
    taktrate: float


class MaschineIn(APIModel):
    name: str
    ruestzeit: float
    kosten_minute: float
    ausfall_wahrscheinlichkeit: float
    mitarbeiter_min: int
    mitarbeiter_max: int
    maschinenbefaehigungen: List[MaschinenBefaehigungIn]


class MaschinenBefaehigungTO(APIModel):
    id: str
    schritt_id: str
    taktrate: float


class MaschineTO(APIModel):
    id: str
    name: str
    ruestzeit: float
    kosten_minute: float
    ausfall_wahrscheinlichkeit: float
    mitarbeiter_min: int
    mitarbeiter_max: int
    maschinenbefaehigungen: List[MaschinenBefaehigungTO]


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=500,
        content={"message": f"{exc.message}"},
    )


@szenario_router.get(
    "/maschinen/",
    response_model=List[MaschineTO],
    status_code=status.HTTP_200_OK,
)
async def read_maschinen(skip: int = 0, take: int = 20):
    async with async_session() as session:
        result = await get_maschinen(session, skip, take)
        return [MaschineTO(**asdict(x)) for x in result]

@szenario_router.get(
    "/maschinen/{maschine_id}",
    response_model=MaschineTO,
    status_code=status.HTTP_200_OK,
)
async def read_maschine(maschine_id: str):
    async with async_session() as session:
        result = await get_maschine(session, maschine_id)
        return MaschineTO(**asdict(result))

@szenario_router.post(
    "/maschinen/",
    response_model=MaschineTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_maschine(maschine: MaschineIn):
    async with async_session() as session:
        maschine_in_dict = maschine.dict()
        maschine_in_dict.pop("maschinenbefaehigungen", None)
        result = await add_maschine(
            session,
            Maschine(
                id=uuid.uuid4().hex,
                **maschine_in_dict,
                maschinenbefaehigungen=[
                    MaschinenBefaehigung(id=uuid.uuid4().hex, **x.dict())
                    for x in maschine.maschinenbefaehigungen
                ],
            ),
        )
        return MaschineTO(**asdict(result))


@szenario_router.delete("/maschinen/{maschine_id}/", status_code=status.HTTP_200_OK)
async def delete_maschine(maschine_id: str):
    async with async_session() as session:
        await remove_maschine(session, maschine_id)
        return {
            "message": "Maschine with id: {} deleted successfully!".format(maschine_id)
        }


class MaterialIn(APIModel):
    name: str
    kosten_stueck: float
    bestand: float
    aufstocken_minute: float


class MaterialTO(APIModel):
    id: str
    name: str
    kosten_stueck: float
    bestand: float
    aufstocken_minute: float


@szenario_router.get(
    "/materialien/",
    response_model=List[MaterialTO],
    status_code=status.HTTP_200_OK,
)
async def read_all_material(skip: int = 0, take: int = 20):
    async with async_session() as session:
        result = await get_all_material(session, skip, take)
        return [MaterialTO(**asdict(x)) for x in result]


@szenario_router.get(
    "/materialien/{material_id}",
    response_model=MaterialTO,
    status_code=status.HTTP_200_OK,
)
async def read_material(material_id: str):
    async with async_session() as session:
        result = await get_material(session, material_id)
        return MaterialTO(**asdict(result))


@szenario_router.post(
    "/materialien/",
    response_model=MaterialTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_material(material: MaterialIn):
    async with async_session() as session:
        result = await add_material(
            session,
            Material(
                id=uuid.uuid4().hex,
                **material.dict(),
            ),
        )
        return MaterialTO(**asdict(result))


@szenario_router.delete("/materialien/{material_id}/", status_code=status.HTTP_200_OK)
async def delete_material(material_id: str):
    async with async_session() as session:
        await remove_material(session, material_id)
        return {
            "message": "Material with id: {} deleted successfully!".format(material_id)
        }


class ProduktionsschrittIn(APIModel):
    schritt: int


class ProduktionsschrittTO(APIModel):
    id: str
    schritt: int


class MaterialbedarfIn(APIModel):
    material_id: str
    menge: float


class MaterialbedarfTO(APIModel):
    id: str
    material_id: str
    menge: float


class ProduktIn(APIModel):
    name: str
    verkaufspreis: float
    produktionsschritte: list[ProduktionsschrittIn]
    materialbedarf: list[MaterialbedarfIn]


class ProduktTO(APIModel):
    id: str
    name: str
    verkaufspreis: float
    produktionsschritte: list[ProduktionsschrittTO]
    materialbedarf: list[MaterialbedarfTO]


def convert_to_produktto(produkt: Produkt) -> ProduktTO:
    return ProduktTO(
        id=produkt.id,
        name=produkt.name,
        verkaufspreis=produkt.verkaufspreis,
        produktionsschritte=[
            ProduktionsschrittTO(**asdict(x)) for x in produkt.produktionsschritte
        ],
        materialbedarf=[
            MaterialbedarfTO(id=x.id, material_id=x.material.id, menge=x.menge)
            for x in produkt.materialbedarf
        ],
    )


@szenario_router.get(
    "/produkte/",
    response_model=List[ProduktTO],
    status_code=status.HTTP_200_OK,
)
async def read_all_produkte(szenario_id: str, skip: int = 0, take: int = 20):
    async with async_session() as session:
        result = await get_all_produkte(session, skip, take)
        return [convert_to_produktto(x) for x in result]


@szenario_router.get(
    "/produkte/{produkt_id}",
    response_model=ProduktTO,
    status_code=status.HTTP_200_OK,
)
async def read_produkt(szenario_id: str, produkt_id: str):
    async with async_session() as session:
        result = await get_produkt(session, produkt_id)
        return convert_to_produktto(result)


@szenario_router.post(
    "/produkte/",
    response_model=ProduktTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_produkt(szenario_id: str, produkt: ProduktIn):
    async with async_session() as session:
        result = await add_produkt(
            session,
            Produkt(
                id=uuid.uuid4().hex,
                name=produkt.name,
                verkaufspreis=produkt.verkaufspreis,
                produktionsschritte=[
                    Produktionsschritt(id=uuid.uuid4().hex, **x.dict())
                    for x in produkt.produktionsschritte
                ],
                materialbedarf=[
                    Materialbedarf(
                        id=uuid.uuid4().hex,
                        material=await get_material(session, x.material_id),
                        menge=x.menge,
                    )
                    for x in produkt.materialbedarf
                ],
            ),
        )

        return convert_to_produktto(result)


class ProduktbedarfIn(APIModel):
    produkt_id: str
    stueckzahl: int


class ChargeIn(APIModel):
    name: str
    prioritaet: int
    produktbedarf: List[ProduktbedarfIn]


class ProduktbedarfTO(APIModel):
    id: str
    produkt_id: str
    stueckzahl: int


class ChargeTO(APIModel):
    id: str
    name: str
    prioritaet: int
    produktbedarf: List[ProduktbedarfTO]


def convert_to_chargeto(charge: Charge) -> ChargeTO:
    return ChargeTO(
        id=charge.id,
        name=charge.name,
        prioritaet=charge.prioritaet,
        produktbedarf=[
            ProduktbedarfTO(id=x.id, produkt_id=x.produkt.id, stueckzahl=x.stueckzahl)
            for x in charge.produktbedarf
        ],
    )


@szenario_router.get(
    "/chargen/",
    response_model=List[ChargeTO],
    status_code=status.HTTP_200_OK,
)
async def read_all_chargen(szenario_id: str, skip: int = 0, take: int = 20):
    async with async_session() as session:
        result = await get_all_chargen(session, skip, take)
        return [convert_to_chargeto(x) for x in result]


@szenario_router.get(
    "/chargen/{charge_id}",
    response_model=ChargeTO,
    status_code=status.HTTP_200_OK,
)
async def read_charge(szenario_id: str, charge_id: str):
    async with async_session() as session:
        result = await get_charge(session, charge_id)
        return convert_to_chargeto(result)


@szenario_router.post(
    "/chargen/",
    response_model=ChargeTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_charge(szenario_id: str, charge: ChargeIn):
    async with async_session() as session:
        result = await add_charge(
            session,
            Charge(
                id=uuid.uuid4().hex,
                name=charge.name,
                prioritaet=charge.prioritaet,
                produktbedarf=[
                    Produktbedarf(
                        id=uuid.uuid4().hex,
                        produkt=await get_produkt(session, x.produkt_id),
                        stueckzahl=x.stueckzahl,
                    )
                    for x in charge.produktbedarf
                ],
            ),
        )

        return convert_to_chargeto(result)


app.include_router(szenario_router)
