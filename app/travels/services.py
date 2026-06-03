from dataclasses import dataclass

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.places.models import TravelProjectPlace
from app.travels.exceptions import (
    CannotDeleteWithVisitedPlacesError,
    TravelProjectNotFoundError,
)
from app.travels.models import TravelProject


@dataclass(kw_only=True)
class TravelProjectService:
    db_session: AsyncSession

    async def get(self, id: int) -> TravelProject | None:
        stmt = select(TravelProject).where(TravelProject.id == id)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all(self) -> list[TravelProject]:
        stmt = select(TravelProject)
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

    async def get_list(self, page: int, size: int = 10) -> list[TravelProject]:
        offset = (page - 1) * size

        stmt = select(TravelProject).limit(size).offset(offset)
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

    async def create(self, **fields) -> TravelProject:
        project = TravelProject(**fields)

        self.db_session.add(project)
        await self.db_session.flush()
        await self.db_session.refresh(project)

        return project

    async def update(self, id: int, **fields) -> TravelProject | None:
        stmt = (
            update(TravelProject)
            .where(TravelProject.id == id)
            .values(**fields)
            .returning(TravelProject)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.flush()

        return result.scalar_one_or_none()

    async def delete(self, id: int):
        project_exists_stmt = select(TravelProject.id).where(TravelProject.id == id)
        project_exists_res = await self.db_session.execute(project_exists_stmt)
        if project_exists_res.scalar_one_or_none() is None:
            raise TravelProjectNotFoundError

        visited_stmt = (
            select(TravelProjectPlace.id)
            .where(TravelProjectPlace.project_id == id, TravelProjectPlace.visited)
            .limit(1)
        )
        visited_res = await self.db_session.execute(visited_stmt)

        if visited_res.scalar_one_or_none() is not None:
            raise CannotDeleteWithVisitedPlacesError

        delete_stmt = delete(TravelProject).where(TravelProject.id == id)
        await self.db_session.execute(delete_stmt)
        await self.db_session.flush()
