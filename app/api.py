from fastapi import APIRouter, Depends, FastAPI

from app.auth.dependencies import verify_credentials
from app.travels.routers import router as travel_router
from app.places.routers import router as place_router


def setup_api(app: FastAPI) -> None:
    api_router = APIRouter(dependencies=[Depends(verify_credentials)])

    api_router.include_router(travel_router, prefix="/travels", tags=["Travels"])
    api_router.include_router(place_router, prefix="/places", tags=["Places"])

    app.include_router(api_router, prefix="/api/v1")
