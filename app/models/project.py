import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class ProjectType(str, Enum):
    PROJECT = "project"
    EXPERIMENT = "exp"


class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: str
    link: str = Field(max_length=500)
    year: int
    type: ProjectType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
