from typing import Annotated

from fastapi import Depends, Request

from app.database.dependencies import DbSessionDep
from app.places.clients import PlacesClient
from app.places.services import TravelProjectPlaceService


def get_place_client(request: Request) -> PlacesClient:
    client = request.app.state.http_client
    return PlacesClient(client=client)


PlacesClientDep = Annotated[PlacesClient, Depends(get_place_client)]


def get_project_place_service(
    db_session: DbSessionDep, place_client: PlacesClientDep
) -> TravelProjectPlaceService:
    return TravelProjectPlaceService(db_session=db_session, place_client=place_client)


ProjectPlaceServiceDep = Annotated[
    TravelProjectPlaceService, Depends(get_project_place_service)
]
