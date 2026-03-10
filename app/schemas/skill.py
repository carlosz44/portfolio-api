import uuid
from datetime import date

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import Field, SQLModel

from app.models.skill import SkillType


class SkillBase(SQLModel):
    title: str = Field(max_length=200)
    start: date
    end: date | None = None
    type: SkillType


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SQLModel):
    title: str | None = None
    start: date | None = None
    end: date | None = None
    type: SkillType | None = None


class SkillRead(SkillBase):
    id: uuid.UUID
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
