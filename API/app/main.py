# https://www.tutlinks.com/fastapi-with-postgresql-crud-async/

from typing import List

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from persistence.database import Base, async_session, engine
from persistence.maschinen import get_maschinen, add_maschine
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# allow_origins=['client-facing-example-app.com', 'localhost:5000']



class MaschinenBefaehigungIn(BaseModel):
    schrittId: str
    taktrate: float


class MaschineIn(BaseModel):
    name: str
    ruestzeit: float
    kostenMinute: float
    ausfallWahrscheinlichkeit: float
    mitarbeiterMin: int
    mitarbeiterMax: int
    maschinenbefaehigung: List[MaschinenBefaehigungIn]


class MaschinenBefaehigung(BaseModel):
    id: str
    schrittId: str
    taktrate: float


class Maschine(BaseModel):
    id: str
    name: str
    ruestzeit: float
    kostenMinute: float
    ausfallWahrscheinlichkeit: float
    mitarbeiterMin: int
    mitarbeiterMax: int
    maschinenbefaehigung: List[MaschinenBefaehigung]





@app.get("/maschinen/", response_model=List[Maschine], status_code=status.HTTP_200_OK)
async def read_maschinen(skip: int = 0, take: int = 20):
    async with async_session() as session:
        return await get_maschinen(session, skip, take)


@app.post("/maschinen/", response_model=Maschine, status_code=status.HTTP_201_CREATED)
async def create_maschine(maschine: MaschineIn):
    async with async_session() as session:
        return await add_maschine(session, maschine)


# @app.delete("/maschinen/{maschine_id}/", status_code=status.HTTP_200_OK)
# async def delete_maschine(maschine_id: int):
#     query = maschinen.delete().where(maschinen.c.id == maschine_id)
#     await database.execute(query)
#     return {
#         "message": "Maschinen with id: {} deleted successfully!".format(maschine_id)
#     }


# @app.put(
#     "/maschinen/{maschine_id}/",
#     response_model=Maschinen,
#     status_code=status.HTTP_200_OK,
# )
# async def update_maschine(maschine_id: int, payload: MaschinenIn):
#     query = (
#         maschinen.update()
#         .where(maschinen.c.id == maschine_id)
#         .values(**payload)
#     )
#     await database.execute(query)
#     return {**payload.dict(), "id": maschine_id}
