import uuid
from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class SkillType(str, Enum):
    FRONT = "front"
    LANGUAGE = "language"
    OTHER = "other"


class Skill(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    start: date
    end: date | None = None
    type: SkillType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
