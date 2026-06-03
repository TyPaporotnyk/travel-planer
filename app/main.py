from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient

from app.api import setup_api

swagger_ui_parameters = {
    "persistAuthorization": True,
    "displayRequestDuration": True,
    "tryItOutEnabled": True,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncClient(base_url="https://api.artic.edu/api/v1/") as client:
        app.state.http_client = client
        yield


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
