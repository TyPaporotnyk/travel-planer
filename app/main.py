from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import Redis

from app.api import setup_api
from app.config import REDIS_URL

swagger_ui_parameters = {
    "persistAuthorization": True,
    "displayRequestDuration": True,
    "tryItOutEnabled": True,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

    async with AsyncClient(base_url="https://api.artic.edu/api/v1/") as client:
        app.state.http_client = client
        app.state.redis_client = redis_client

        yield

    await redis_client.close()


app = FastAPI(
    title="Travel planer",
    description="Travel planer api's documentation",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters=swagger_ui_parameters,
    lifespan=lifespan,
)

setup_api(app)


@app.get("/health")
async def health():
    return {"status": "ok"}
