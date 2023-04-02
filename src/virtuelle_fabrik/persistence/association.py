from sqlalchemy import Column, ForeignKey, String, Table
from .database import Base


station_maschine_association_table = Table(
    "station_maschine_association_table",
    Base.metadata,
    Column("station_id", String, ForeignKey("stationen.id"), primary_key=True),
    Column("maschine_id", String, ForeignKey("maschinen.id"), primary_key=True),
)