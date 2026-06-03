from fastapi import APIRouter, FastAPI

from app.travels.routers import router as travel_router
from app.places.routers import router as place_router


def setup_api(app: FastAPI) -> None:
    api_router = APIRouter()

    api_router.include_router(travel_router, prefix="/travels", tags=["Travels"])
    api_router.include_router(place_router, prefix="/places", tags=["Places"])

    app.include_router(api_router, prefix="/api/v1")
