import uuid
from datetime import date

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import Field, SQLModel


class WorkBase(SQLModel):
    company: str = Field(max_length=200)
    role: str = Field(max_length=200)
    description: str
    start: date
    end: date | None = None
    location: str = Field(max_length=200)
    tech_stack: str = Field(default="", max_length=500)


class WorkCreate(WorkBase):
    pass


class WorkUpdate(SQLModel):
    company: str | None = None
    role: str | None = None
    description: str | None = None
    start: date | None = None
    end: date | None = None
    location: str | None = None
    tech_stack: str | None = None


class WorkRead(WorkBase):
    id: uuid.UUID
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
