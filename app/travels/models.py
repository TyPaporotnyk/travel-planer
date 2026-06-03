from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database.core import BaseModel
from app.database.mixins import TimeStampMixin


class TravelProject(BaseModel, TimeStampMixin):
    __tablename__ = "travel_projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
