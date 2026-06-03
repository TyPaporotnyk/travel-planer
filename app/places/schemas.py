from pydantic import BaseModel


class BaseProjectPlaceSchema(BaseModel):
    external_place_id: str
    notes: str | None = None
    visited: bool = False


class ResponseProjectPlaceSchema(BaseProjectPlaceSchema):
    id: int
    project_id: int


class CreatePlaceWithProjectSchema(BaseProjectPlaceSchema):
    pass


class CreateProjectPlaceSchema(BaseProjectPlaceSchema):
    project_id: int


class UpdatePlaceSchema(BaseModel):
    notes: str | None = None
    visited: bool | None = None
