from typing import Annotated

from fastapi import Depends

from app.database.dependencies import DbSessionDep
from app.travels.services import TravelProjectService


def get_travel_project_service(db_session: DbSessionDep) -> TravelProjectService:
    return TravelProjectService(db_session=db_session)


TravelProjectServiceDep = Annotated[TravelProjectService, Depends(get_travel_project_service)]
