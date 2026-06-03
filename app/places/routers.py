from fastapi import APIRouter, HTTPException, status

from app.places.dependencies import ProjectPlaceServiceDep
from app.places.exceptions import ProjectPlaceNotFoundError
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
    place = await service.create(**data.model_dump())

    if not place:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid external_place_id or place not found in external API",
        )

    return ApiResponse(data=place)


@router.get("", response_model=ApiResponse[list[ResponseProjectPlaceSchema]])
async def get_travel_project_places(
    project_id: int,
    service: ProjectPlaceServiceDep,
):
    places = await service.get_by_project(project_id=project_id)

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
