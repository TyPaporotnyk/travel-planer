from fastapi import APIRouter, HTTPException, status

from app.places.dependencies import ProjectPlaceServiceDep
from app.places.exceptions import DuplicatePlaceInProjectError, MaxPlacesExceededError, PlaceValidationError
from app.schemas import ApiResponse
from app.travels.dependencies import TravelProjectServiceDep
from app.travels.exceptions import (
    CannotDeleteWithVisitedPlacesError,
    TravelProjectNotFoundError,
)
from app.travels.schemas import (
    CreateTravelSchema,
    ResponseTravelSchema,
    UpdateTravelSchema,
)

router = APIRouter()


@router.post(
    "",
    response_model=ApiResponse[ResponseTravelSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_travel_project(
    data: CreateTravelSchema,
    project_service: TravelProjectServiceDep,
    place_service: ProjectPlaceServiceDep,
):
    project_fields = data.model_dump(exclude={"places"})
    project = await project_service.create(**project_fields)

    if data.places:
        places_data = [place.model_dump() for place in data.places]

        try:
            await place_service.create_many(project.id, places_data)
        except PlaceValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid external_place_id or place not found in external API.",
            ) from exc
        except MaxPlacesExceededError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 10 places allowed per project.",
            ) from exc
        except DuplicatePlaceInProjectError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This external place is already linked to the project.",
            ) from exc

    return ApiResponse(data=project)


@router.get("/{id}", response_model=ApiResponse[ResponseTravelSchema])
async def get_travel_project(
    id: int,
    service: TravelProjectServiceDep,
):
    project = await service.get(id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Travel project not found",
        )

    return ApiResponse(data=project)


@router.get("", response_model=ApiResponse[list[ResponseTravelSchema]])
async def get_travel_projects(
    service: TravelProjectServiceDep,
):
    projects = await service.get_all()

    return ApiResponse(data=projects)


@router.patch("/{id}", response_model=ApiResponse[ResponseTravelSchema])
async def update_travel_project(
    id: int,
    data: UpdateTravelSchema,
    service: TravelProjectServiceDep,
):
    project = await service.update(
        id=id,
        **data.model_dump(exclude_unset=True),
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Travel project not found",
        )

    return ApiResponse(data=project)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_travel_project(
    id: int,
    service: TravelProjectServiceDep,
):
    try:
        await service.delete(id)
    except TravelProjectNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Travel project not found") from exc
    except CannotDeleteWithVisitedPlacesError as exc:
        raise HTTPException(
            status_code=400, detail="Cannot delete project with visited places"
        ) from exc

    return None
