"""Test configuration and shared fixtures.

Key concepts:
- conftest.py is auto-discovered by pytest — no imports needed in test files.
- Fixtures are reusable setup functions injected by name into test parameters.
- `yield` in a fixture means: everything before yield = setup, after = teardown.
- `scope="session"` means the fixture runs once for the entire test suite.
- `scope="function"` (default) means it runs before each test function.
"""

import os

# Set environment variables BEFORE importing app modules.
# pydantic-settings reads env vars at import time, so these must be set first.
os.environ.update({
    "DB_USER": "test",
    "DB_PASSWORD": "test",
    "DB_HOST": "localhost",
    "DB_NAME": "test",
    "SECRET_KEY": "test-secret-key-for-jwt",
    "CORS_ORIGINS": '["http://localhost:3000"]',
    "ENVIRONMENT": "testing",
})

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.auth.service import create_access_token, hash_password
from app.database import get_session
from app.main import app
# Import ALL models so SQLModel.metadata knows about them when creating tables.
# Without these imports, create_all() won't create the corresponding tables.
from app.models.project import Project  # noqa: F401
from app.models.skill import Skill  # noqa: F401
from app.models.user import User
from app.models.work import Work  # noqa: F401


# SQLite in-memory database for tests.
# - `check_same_thread=False`: SQLite only allows access from the creating thread
#   by default, but FastAPI runs endpoints in a thread pool.
# - `StaticPool`: Forces all connections to share the SAME in-memory database.
#   Without this, each connection gets its own empty database.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="function")
def session():
    """Create a fresh database for each test.

    - Creates all tables before the test
    - Yields a session for the test to use
    - Drops all tables after the test (clean slate)
    """
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def client(session: Session):
    """FastAPI test client with the database session overridden.

    `app.dependency_overrides` lets us swap any Depends() function
    with a test version. Here we replace get_session so all endpoints
    use our SQLite test database instead of the real PostgreSQL.
    """

    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(session: Session) -> User:
    """Create a test user in the database."""
    user = User(
        username="testuser",
        hashed_password=hash_password("testpassword"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture()
def auth_headers(test_user: User) -> dict[str, str]:
    """Generate an Authorization header with a valid JWT for the test user.

    This is used in tests for protected endpoints (POST, PATCH, DELETE).
    """
    token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {token}"}
