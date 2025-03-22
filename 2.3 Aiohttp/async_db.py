import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

# Асинхронный движок для SQLite
engine = create_async_engine('sqlite+aiosqlite:///2.3 Aiohttp/db/Aiohttp.db', echo=True)

# Асинхронная сессия
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    token = Column(String, unique=True)

class Advertisment(Base):
    __tablename__ = "advertisment"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user = Column(Integer, ForeignKey('user.id'))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()