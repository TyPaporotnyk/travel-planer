from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint, false
from sqlalchemy.orm import Mapped, mapped_column

from app.database.core import BaseModel
from app.database.mixins import TimeStampMixin


class TravelProjectPlace(BaseModel, TimeStampMixin):
    __tablename__ = "travel_project_places"
    __table_args__ = (
        UniqueConstraint("project_id", "external_place_id", name="uq_project_place"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("travel_projects.id"),
        index=True,
        nullable=False,
    )

    external_place_id: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    visited: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )
