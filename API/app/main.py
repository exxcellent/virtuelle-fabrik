from typing import List
import uuid
from attrs import asdict


from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from API.app.src.domain.exception import DomainException
from API.app.src.domain.models import Maschine, MaschinenBefaehigung
from API.app.src.persistence.database import async_session
from API.app.src.persistence.maschinen import get_maschinen, add_maschine, remove_maschine
from pydantic import BaseConfig, BaseModel


app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/maschinen/", response_model=List[MaschineTO], status_code=status.HTTP_200_OK)
async def read_maschinen(skip: int = 0, take: int = 20):
    async with async_session() as session:
        result = await get_maschinen(session, skip, take)
        return [MaschineTO(**asdict(x)) for x in result]


@app.post("/maschinen/", response_model=MaschineTO, status_code=status.HTTP_201_CREATED)
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
                ]
            ),
        )
        return MaschineTO(**asdict(result))


@app.delete("/maschinen/{maschine_id}/", status_code=status.HTTP_200_OK)
async def delete_maschine(maschine_id: str):
    async with async_session() as session:
        await remove_maschine(session, maschine_id)
        return {
            "message": "Maschine with id: {} deleted successfully!".format(maschine_id)
        }
