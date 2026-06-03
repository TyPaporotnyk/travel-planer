from fastapi import APIRouter, FastAPI



def setup_api(app: FastAPI) -> None:
    api_router = APIRouter()

    app.include_router(api_router, prefix="/api/v1")
