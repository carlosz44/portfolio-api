# portfolio-api

A FastAPI CMS API for portfolio content: projects, skills and work experience. Reads are public and writes need a JWT. web doesn't use it (it keeps its own data in Supabase), and it isn't deployed: the README describes a Vercel and Neon setup, but no deployment exists.

Adds to `~/Dev/CLAUDE.md` and never contradicts it. Notes live in `~/Dev/dev-workspace/projects/portfolio-api/`.

## Commands

- `cp .env.example .env`, then set a real `SECRET_KEY`
- `docker compose up --build`: the API on `localhost:8000` and Postgres on host port `DB_PORT` (5432 by default). baby-tracker binds both ports too, so only one of them runs at a time
- `docker compose exec api uv run alembic upgrade head`: apply migrations
- `docker compose exec api uv run alembic revision --autogenerate -m "<what changed>"`: a new migration after a model change
- `docker compose exec api uv run python -m app.seed`: seed from `seed_data.json`, whose format is in `seed_data.example.json`
- `uv run pytest tests/ -v`: tests on in-memory SQLite, no Docker needed
- `uv run ruff check .` and `uv run ruff format .`
- API docs: `localhost:8000/docs` and `localhost:8000/redoc`

## Architecture

The FastAPI app starts in `app/main.py`. Each resource has a SQLModel model in `app/models/`, Pydantic request and response schemas in `app/schemas/` and a router in `app/routers/`. `app/auth/` handles login, JWTs (python-jose) and password hashing (bcrypt). `app/dependencies.py` holds the auth guard that write endpoints depend on. Settings come from environment variables through `app/config.py`, and `.env.example` lists them.

Endpoints: `GET /` is the health check and `POST /auth/login` returns a JWT. `/projects/` (filter `type=project` or `exp`), `/skills/` (filter `type=front`, `language` or `other`) and `/work/` (newest start first) each support GET, POST, PATCH and DELETE. GET is public, and the rest need the JWT.

## Guardrails

- This repo is public. `.env` and `seed_data.json` are gitignored and stay that way. Hosts in docs stay placeholders, like the README's `ep-xxx` Neon host.
- Python 3.12 or newer, managed with uv.

## Definition of done

- `uv run pytest tests/` and `uv run ruff check .` pass.
