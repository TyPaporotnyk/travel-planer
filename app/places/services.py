import asyncio
from dataclasses import dataclass

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.places.clients import PlacesClient
from app.places.exceptions import PlaceValidationError, ProjectPlaceNotFoundError
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

    async def create(self, **fields) -> TravelProjectPlace | None:
        external_id = fields.get("external_place_id")
        if external_id and not await self.place_client.validate_place(external_id):
            return None

        place = TravelProjectPlace(**fields)

        self.db_session.add(place)
        await self.db_session.flush()
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

        await self.db_session.flush()

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

        if result.scalar_one_or_none() is not None:
            raise ProjectPlaceNotFoundError
