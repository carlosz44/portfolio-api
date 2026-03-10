import uuid
from datetime import date, datetime

from sqlmodel import Field, SQLModel


class Work(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    company: str = Field(max_length=200)
    role: str = Field(max_length=200)
    description: str
    start: date
    end: date | None = None
    location: str = Field(max_length=200)
    tech_stack: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
