from datetime import date

from pydantic import BaseModel, Field

from app.places.schemas import CreatePlaceWithProjectSchema


class BaseTravelSchema(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None


class ResponseTravelSchema(BaseTravelSchema):
    id: int


class CreateTravelSchema(BaseTravelSchema):
    places: list[CreatePlaceWithProjectSchema] = Field(default_factory=list)


class UpdateTravelSchema(BaseTravelSchema): ...
