# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview
This project is an enterprise task management system (like Jira). The main goal is to be used as a portfolio on github.
The project should be considered as an enterprise and real world system in the industry.

## Architecture

### Hexagonal Architecture + DDD

Two bounded contexts: `user_management` and `task_management`. Each is fully self-contained — no shared domain objects across contexts. Cross-context references use IDs (plain values), never aggregate objects.

Layer dependency rule: `domain ← application ← adapters / infrastructure`. The domain imports nothing from outer layers.

```
src/app/
├── core/                  # DomainError base, Settings
├── infrastructure/        # Shared DB engine & session factory
├── interfaces/http/       # Shared FastAPI exception handler + APIException
├── container.py           # Manual DI wiring (attached to app.container at startup)
├── main.py                # App factory + lifespan
└── {context}/
    ├── domain/            # Entities, value objects, domain ports (ABCs), domain exceptions
    ├── application/       # Use cases, application services, commands, DTOs, app ports
    ├── infrastructure/    # SQL adapters, ORM models, security implementations
    └── adapters/driving/  # FastAPI controllers, schemas, FastAPI dependencies
```

## Roadmap

At the end of the project below points **must** be completed:
- Task management system with at least two bounded contexts (task & User).
- Events should be used (based on DDD) to communicate between different parts and contexts.
- At least two driving adapters (HTTP & another one), should be available to interact with the system.
- Background jobs to handle some parts of the system.
- Eventually each bounded context should be split into a microservice.
- A real DI container to be used instead of the manual one

## Commands

```bash
# Run all unit tests (no DB required, default)
pytest -m unit

# Run integration tests (requires PostgreSQL)
pytest -m integration

# Run a single test file
pytest tests/path/to/test_file.py -m unit

# Run a single test by name
pytest tests/path/to/test_file.py::test_name -m unit

# Lint
ruff check src/ tests/

# Format check
ruff format --check src/ tests/

# Format (fix)
ruff format src/ tests/

# Run migrations
alembic upgrade head

# Start local dev environment
docker compose -f docker-compose.dev.yml up -d

# Start the API server (local, no Docker)
uvicorn src.app.main:app --reload
```

Every test **must** be marked `@pytest.mark.unit` or `@pytest.mark.integration` — the conftest enforces this and will fail unmarked tests. Integration tests are skipped unless explicitly run with `-m integration`.

Tests require a `tests/.env` file (see `.env.example`).


### Key patterns — quick reference

**Dependency rule**: `domain ← application ← adapters / infrastructure`. Domain imports nothing from outer layers.

**Cross-context**: bounded contexts share no domain objects. Reference by plain ID value only.

**Exception flow**: `DomainError` subclass → global handler → `_DOMAIN_TO_HTTP` lookup → `APIException`. See `src/app/CLAUDE.md` for details.

**Value objects**: frozen Pydantic models. Invalid construction raises a domain exception, never a raw `ValidationError`. See `{context}/domain/CLAUDE.md`.

**ORM isolation**: SQLAlchemy models in `infrastructure/persistence/models.py` only. Map via `from_entity()` / `to_entity()`. Domain never imports SQLAlchemy.

**Tests**: every test marked `@pytest.mark.unit` or `@pytest.mark.integration`. See `tests/CLAUDE.md`.

## Current sprint

`.claude/sprints/sprint_2.md`

