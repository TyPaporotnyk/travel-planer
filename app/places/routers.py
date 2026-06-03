from fastapi import APIRouter, HTTPException, Query, status

from app.places.dependencies import ProjectPlaceServiceDep
from app.places.exceptions import (
    DuplicatePlaceInProjectError,
    MaxPlacesExceededError,
    PlaceValidationError,
    ProjectPlaceNotFoundError,
)
from app.places.schemas import (
    CreateProjectPlaceSchema,
    ResponseProjectPlaceSchema,
    UpdatePlaceSchema,
)
from app.schemas import ApiResponse

router = APIRouter()


@router.post(
    "",
    response_model=ApiResponse[ResponseProjectPlaceSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_travel_project_place(
    data: CreateProjectPlaceSchema,
    service: ProjectPlaceServiceDep,
):
    try:
        place = await service.create(**data.model_dump())
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

    return ApiResponse(data=place)


@router.get("", response_model=ApiResponse[list[ResponseProjectPlaceSchema]])
async def get_travel_project_places(
    project_id: int,
    service: ProjectPlaceServiceDep,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    places = await service.get_list(
        project_id=project_id,
        page=page,
        size=size
    )

    return ApiResponse(data=places)


@router.get("/{id}", response_model=ApiResponse[ResponseProjectPlaceSchema])
async def get_travel_project_place(
    id: int,
    service: ProjectPlaceServiceDep,
):
    place = await service.get(place_id=id)

    print(place)

    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project place not found",
        )

    return ApiResponse(data=place)


@router.patch("/{id}", response_model=ApiResponse[ResponseProjectPlaceSchema])
async def update_travel_project_place(
    id: int,
    data: UpdatePlaceSchema,
    service: ProjectPlaceServiceDep,
):
    place = await service.update(
        place_id=id,
        **data.model_dump(exclude_unset=True),
    )

    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project place not found",
        )

    return ApiResponse(data=place)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_travel_project_place(
    id: int,
    service: ProjectPlaceServiceDep,
):
    try:
        await service.delete(place_id=id)
    except ProjectPlaceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project place not found",
        ) from exc
