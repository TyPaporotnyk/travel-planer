import logging

from starlette.config import Config

logger = logging.getLogger(__name__)
config = Config(".env")

DATABASE_NAME = config("DATABASE_NAME")
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

REDIS_HOST = config("REDIS_HOST", default="127.0.0.1")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_DB = config("REDIS_DB", cast=int, default=0)
REDIS_PASSWORD = config("REDIS_PASSWORD", cast=str, default="")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

MAX_PROJECT_PLACES_COUNT = 10
