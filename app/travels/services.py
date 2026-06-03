from dataclasses import dataclass

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def create(self, **fields) -> TravelProject:
        project = TravelProject(**fields)

        self.db_session.add(project)
        await self.db_session.commit()
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
        await self.db_session.commit()

        return result.scalar_one_or_none()

    async def delete(self, id: int) -> bool:
        stmt = (
            delete(TravelProject)
            .where(TravelProject.id == id)
            .returning(TravelProject.id)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.commit()

        return result.scalar_one_or_none() is not None
