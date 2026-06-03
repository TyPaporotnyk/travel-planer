from datetime import date

from pydantic import BaseModel


class BaseTravelSchema(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None


class ResponseTravelSchema(BaseTravelSchema):
    id: int


class CreateTravelSchema(BaseTravelSchema): ...


class UpdateTravelSchema(BaseTravelSchema): ...
