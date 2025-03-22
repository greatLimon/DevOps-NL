import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, JSON

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT','5431')

PG_DSN = (f'postgresql+asyncpg://'
          f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
          f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
          )

engine = create_async_engine(PG_DSN)
db_session = async_sessionmaker(bind = engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass

#MODELS:
class SwapiPeople(Base):
    __tablename__ = 'swapi_people'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    json_data: Mapped[dict] = mapped_column(JSON)

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()