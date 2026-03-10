import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, max_length=50)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
