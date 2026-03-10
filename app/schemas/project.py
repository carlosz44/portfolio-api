import uuid

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import Field, SQLModel

from app.models.project import ProjectType


class ProjectBase(SQLModel):
    title: str = Field(max_length=200)
    description: str
    link: str = Field(max_length=500)
    year: int = Field(ge=2000, le=2100)
    type: ProjectType


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    link: str | None = None
    year: int | None = Field(default=None, ge=2000, le=2100)
    type: ProjectType | None = None


class ProjectRead(ProjectBase):
    id: uuid.UUID
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
