import asyncio
from dataclasses import dataclass

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import MAX_PROJECT_PLACES_COUNT
from app.places.clients import PlacesClient
from app.places.exceptions import (
    DuplicatePlaceInProjectError,
    MaxPlacesExceededError,
    PlaceValidationError,
    ProjectPlaceNotFoundError,
)
from app.places.models import TravelProjectPlace


@dataclass(kw_only=True)
class TravelProjectPlaceService:
    db_session: AsyncSession
    place_client: PlacesClient

    async def get(self, place_id: int) -> TravelProjectPlace | None:
        stmt = select(TravelProjectPlace).where(TravelProjectPlace.id == place_id)

        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_project(self, project_id: int) -> list[TravelProjectPlace]:
        stmt = select(TravelProjectPlace).where(
            TravelProjectPlace.project_id == project_id
        )

        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_list(
        self, project_id: int, page: int, size: int = 10
    ) -> list[TravelProjectPlace]:
        offset = (page - 1) * size

        stmt = (
            select(TravelProjectPlace)
            .where(TravelProjectPlace.project_id == project_id)
            .limit(size)
            .offset(offset)
        )

        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **fields) -> TravelProjectPlace:
        external_id = fields.get("external_place_id")
        project_id = fields.get("project_id")

        current_count = await self.get_places_count(project_id)  # type: ignore
        if current_count + 1 > MAX_PROJECT_PLACES_COUNT:
            raise MaxPlacesExceededError

        if external_id and not await self.place_client.validate_place(external_id):
            raise PlaceValidationError

        place = TravelProjectPlace(**fields)
        self.db_session.add(place)

        try:
            async with self.db_session.begin_nested():
                await self.db_session.flush()
        except IntegrityError as exc:
            raise DuplicatePlaceInProjectError from exc

        await self.db_session.refresh(place)

        return place

    async def create_many(
        self, project_id: int, places_data: list[dict]
    ) -> list[TravelProjectPlace] | None:
        if not places_data:
            return []

        unique_external_ids = list(
            {p["external_place_id"] for p in places_data if "external_place_id" in p}
        )

        if len(places_data) != len(unique_external_ids):
            raise DuplicatePlaceInProjectError

        current_count = await self.get_places_count(project_id)
        if current_count + len(unique_external_ids) > MAX_PROJECT_PLACES_COUNT:
            raise MaxPlacesExceededError

        validation_tasks = [
            self.place_client.validate_place(ext_id) for ext_id in unique_external_ids
        ]
        validation_results = await asyncio.gather(*validation_tasks)
        if not all(validation_results):
            raise PlaceValidationError

        places = []
        for data in places_data:
            place = TravelProjectPlace(project_id=project_id, **data)
            self.db_session.add(place)
            places.append(place)

        try:
            async with self.db_session.begin_nested():
                await self.db_session.flush()
        except IntegrityError as exc:
            raise DuplicatePlaceInProjectError from exc

        for place in places:
            await self.db_session.refresh(place)

        return places

    async def update(self, place_id: int, **fields) -> TravelProjectPlace | None:
        stmt = (
            update(TravelProjectPlace)
            .where(TravelProjectPlace.id == place_id)
            .values(**fields)
            .returning(TravelProjectPlace)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.flush()

        return result.scalar_one_or_none()

    async def delete(self, place_id: int):
        stmt = (
            delete(TravelProjectPlace)
            .where(TravelProjectPlace.id == place_id)
            .returning(TravelProjectPlace.id)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.flush()

        if result.scalar_one_or_none() is None:
            raise ProjectPlaceNotFoundError

    async def get_places_count(self, project_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(TravelProjectPlace)
            .where(TravelProjectPlace.project_id == project_id)
        )
        result = await self.db_session.execute(stmt)

        return result.scalar() or 0
