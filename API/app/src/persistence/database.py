from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/DB"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()