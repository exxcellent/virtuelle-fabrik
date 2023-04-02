from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARN)

def get_db_url_from_env():
    DEFAULT_DB_URL = "postgresql+asyncpg://user:password@localhost:5432/DB"
    import os

    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_user = os.environ.get("DB_USER")
    db_pwd = os.environ.get("DB_PWD")
    db_name = os.environ.get("DB_NAME")
    if None not in [db_host, db_port, db_user, db_pwd, db_name]:
        return f"postgresql+asyncpg://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
    
    return DEFAULT_DB_URL


DATABASE_URL = get_db_url_from_env()

engine = create_async_engine(DATABASE_URL, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()