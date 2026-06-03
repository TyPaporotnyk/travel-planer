from fastapi import APIRouter, HTTPException, status

from app.schemas import ApiResponse
from app.travels.dependencies import TravelProjectServiceDep
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
    service: TravelProjectServiceDep,
):
    project = await service.create(**data.model_dump())

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
    deleted = await service.delete(id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Travel project not found",
        )
