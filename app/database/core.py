from collections.abc import AsyncGenerator

from sqlalchemy import MetaData, NullPool
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app import config

INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


def create_db_engine(connection_string: str):
    url = make_url(connection_string)

    timeout_kwargs = {
        "poolclass": NullPool,
        "pool_pre_ping": True,
    }

    return create_async_engine(url, **timeout_kwargs)


engine = create_db_engine(
    config.SQLALCHEMY_DATABASE_URI,
)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


class BaseModel(DeclarativeBase):
    metadata = MetaData(naming_convention=INDEXES_NAMING_CONVENTION)
