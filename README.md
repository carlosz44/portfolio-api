# Portfolio API

Personal portfolio CMS API built with FastAPI, SQLModel, and PostgreSQL.

## Tech Stack

- **FastAPI** — web framework with automatic OpenAPI docs
- **SQLModel** — ORM combining SQLAlchemy + Pydantic
- **PostgreSQL** — production database (SQLite for tests)
- **Alembic** — database migrations
- **Docker + docker-compose** — local development environment
- **uv** — Python package manager
- **bcrypt + python-jose** — password hashing and JWT authentication
- **Ruff** — linter and formatter
- **pytest** — testing (31 tests)

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | No | Health check |
| POST | `/auth/login` | No | Get JWT token |
| GET | `/projects/` | No | List projects grouped by type |
| GET | `/projects/?type=exp` | No | Filter by type (`project` or `exp`) |
| GET | `/projects/{id}` | No | Get project by ID |
| POST | `/projects/` | Yes | Create project |
| PATCH | `/projects/{id}` | Yes | Update project |
| DELETE | `/projects/{id}` | Yes | Delete project |
| GET | `/skills/` | No | List skills grouped by type |
| GET | `/skills/?type=front` | No | Filter by type (`front`, `language`, `other`) |
| GET | `/skills/{id}` | No | Get skill by ID |
| POST | `/skills/` | Yes | Create skill |
| PATCH | `/skills/{id}` | Yes | Update skill |
| DELETE | `/skills/{id}` | Yes | Delete skill |
| GET | `/work/` | No | List work experience (sorted by start desc) |
| GET | `/work/{id}` | No | Get work by ID |
| POST | `/work/` | Yes | Create work experience |
| PATCH | `/work/{id}` | Yes | Update work experience |
| DELETE | `/work/{id}` | Yes | Delete work experience |

## Setup

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (for running tests locally)

### 1. Environment variables

```bash
cp .env.example .env
```

Edit `.env` and set a secure `SECRET_KEY`.

### 2. Start the containers

```bash
docker compose up --build
```

This starts the API on `http://localhost:8000` and PostgreSQL on port `5432`.

### 3. Run migrations

```bash
docker compose exec api uv run alembic upgrade head
```

### 4. Seed the database (optional)

Create a `seed_data.json` file (see `seed_data.example.json` for the format):

```bash
docker compose exec api uv run python -m app.seed
```

### 5. API docs

Once running, interactive docs are at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Run tests

Tests use SQLite in-memory (no Docker needed):

```bash
uv run pytest tests/ -v
```

### Lint and format

```bash
uv run ruff check .
uv run ruff format .
```

### Create a new migration

After modifying models:

```bash
docker compose exec api uv run alembic revision --autogenerate -m "description"
docker compose exec api uv run alembic upgrade head
```

## Deployment (Vercel)

Vercel auto-detects the FastAPI app from `app/main.py` — no extra config needed.

### 1. Create a Neon PostgreSQL database

Go to [neon.tech](https://neon.tech) and create a new project. Copy the connection details.

### 2. Set environment variables in Vercel

In your Vercel project settings, add:

| Variable | Value |
|----------|-------|
| `DB_USER` | Your Neon username |
| `DB_PASSWORD` | Your Neon password |
| `DB_HOST` | Your Neon host (e.g. `ep-xxx.us-east-2.aws.neon.tech`) |
| `DB_PORT` | `5432` |
| `DB_NAME` | Your database name |
| `SECRET_KEY` | A random 32+ character string |
| `CORS_ORIGINS` | `["https://yourdomain.com"]` |
| `ENVIRONMENT` | `production` |

### 3. Deploy

Connect the GitHub repo to Vercel or use the CLI:

```bash
npx vercel deploy
```

### 4. Run migrations on production

Connect to Neon and run migrations locally pointing to the production database:

```bash
DB_HOST=ep-xxx.us-east-2.aws.neon.tech DB_USER=... DB_PASSWORD=... DB_NAME=... uv run alembic upgrade head
```

## Project Structure

```
app/
├── auth/           # Authentication (login, JWT, password hashing)
├── models/         # SQLModel database models
├── routers/        # API route handlers (CRUD endpoints)
├── schemas/        # Pydantic request/response schemas
├── config.py       # Settings from environment variables
├── database.py     # Database engine and session
├── dependencies.py # FastAPI dependencies (auth guard)
├── main.py         # FastAPI app entry point
└── seed.py         # Database seeding script
migrations/         # Alembic migration files
tests/              # pytest test suite
```
